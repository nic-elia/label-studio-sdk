import copy
import logging
import re
import jsonschema

from typing import Dict, Optional, List, Tuple, Any, Callable, Union
from pydantic import BaseModel

# from typing import Dict, Optional, List, Tuple, Any
from collections import defaultdict
from lxml import etree

from label_studio_sdk.exceptions import (
    LSConfigParseException,
    LabelStudioXMLSyntaxErrorSentryIgnored,
    LabelStudioValidationErrorSentryIgnored)

from label_studio_sdk.label_config.control_tags import ControlTag, ChoicesTag, LabelsTag
from label_studio_sdk.label_config.object_tags import ObjectTag
from label_studio_sdk.label_config.label_tags import LabelTag

RESULT_KEY = "result"

_LABEL_CONFIG_SCHEMA = ""
# = find_file('schema/label_config_schema.json')
# with open(_LABEL_CONFIG_SCHEMA) as f:
#     _LABEL_CONFIG_SCHEMA_DATA = json.load(f)

_LABEL_TAGS = {'Label', 'Choice', 'Relation'}

_DIR_APP_NAME = 'label-studio'
_VIDEO_TRACKING_TAGS = set('videorectangle')


class AnnotationValue(BaseModel):
    """
    """
    result: Optional[List[dict]]
    
        
class PredictionValue(BaseModel):
    """
    """
    model_version: Optional[str]
    score: Optional[float]
    result: Optional[List[dict]]


class TaskValue(BaseModel):
    """
    """
    data: Optional[dict]
    annotations: Optional[List[AnnotationValue]]
    predictions: Optional[List[PredictionValue]]

############ core/label_config.py

def merge_labels_counters(dict1, dict2):
    """
    Merge two dictionaries with nested dictionary values into a single dictionary.

    Args:
        dict1 (dict): The first dictionary to merge.
        dict2 (dict): The second dictionary to merge.

    Returns:
        dict: A new dictionary with the merged nested dictionaries.

    Example:
        dict1 = {'sentiment': {'Negative': 1, 'Positive': 1}}
        dict2 = {'sentiment': {'Positive': 2, 'Neutral': 1}}
        result_dict = merge_nested_dicts(dict1, dict2)
        # {'sentiment': {'Negative': 1, 'Positive': 3, 'Neutral': 1}}
    """
    result_dict = {}

    # iterate over keys in both dictionaries
    for key in set(dict1.keys()) | set(dict2.keys()):
        # add the corresponding values if they exist in both dictionaries
        value = {}
        if key in dict1:
            value.update(dict1[key])
        if key in dict2:
            for subkey in dict2[key]:
                value[subkey] = value.get(subkey, 0) + dict2[key][subkey]
        # add the key-value pair to the result dictionary
        result_dict[key] = value

    return result_dict

def _fix_choices(config):
    """
    workaround for single choice
    https://github.com/heartexlabs/label-studio/issues/1259
    """
    if 'Choices' in config:
        # for single Choices tag in View
        if 'Choice' in config['Choices'] and not isinstance(config['Choices']['Choice'], list):
            config['Choices']['Choice'] = [config['Choices']['Choice']]
        # for several Choices tags in View
        elif isinstance(config['Choices'], list) and all('Choice' in tag_choices for tag_choices in config['Choices']):
            for n in range(len(config['Choices'])):
                # check that Choices tag has only 1 choice
                if not isinstance(config['Choices'][n]['Choice'], list):
                    config['Choices'][n]['Choice'] = [config['Choices'][n]['Choice']]
    if 'View' in config:
        if isinstance(config['View'], OrderedDict):
            config['View'] = _fix_choices(config['View'])
        else:
            config['View'] = [_fix_choices(view) for view in config['View']]
    return config

def get_annotation_tuple(from_name, to_name, type):
    if isinstance(to_name, list):
        to_name = ','.join(to_name)
    return '|'.join([from_name, to_name, type.lower()])

def get_all_control_tag_tuples(label_config):
    # "chc|text|choices"
    outputs = parse_config(label_config)
    out = []
    for control_name, info in outputs.items():
        out.append(get_annotation_tuple(control_name, info['to_name'], info['type']))
    return out

def get_all_types(label_config):
    """
    Get all types from label_config
    """
    outputs = parse_config(label_config)
    out = []
    for control_name, info in outputs.items():
        out.append(info['type'].lower())
    return out

def display_count(count: int, type: str) -> Optional[str]:
    """Helper for displaying pluralized sources of validation errors,
    eg "1 draft" or "3 annotations"
    """
    if not count:
        return None

    return f'{count} {type}{"s" if count > 1 else ""}'

######################

class LabelingConfig():
    """This class parses the config into more logical OOP based
    representation. Since labeling config includes both presentation
    and logic combined, in its parsed form we care only about the
    logic, and less so about the presentation

    """
    def __init__(self, config: str, *args, **kwargs):
        """ """
        self._config = config

        # extract predefined task from the config
        _task_data, _ann, _pred = LabelingConfig.get_task_from_labeling_config(config)
        self._sample_config_task = _task_data
        self._sample_config_ann = _ann
        self._sample_config_pred = _pred
        
        
        controls, objects, labels, tree = self.parse(config)
        controls = self._link_controls(controls, objects, labels)

        
        # list of control tags that this config has
        self._control_tags = set(controls.keys())
        self._object_tags = set(objects.keys())
        # self._label_names = set(labels.keys())
        
        self._controls = controls
        self._objects = objects
        self._labels = labels
        self._tree = tree
        
    ##### NEW API

    @property
    def controls(self):
        """ """
        return self._controls and self._controls.values()

    @property
    def objects(self):
        """ """
        return self._objects and self._objects.values()

    @property
    def labels(self):
        """ """
        return self._labels and self._labels.values()
    
    def _link_controls(self, controls: Dict, objects: Dict, labels: Dict) -> Dict:
        """
        """
        for name, tag in controls.items():
            inputs = []
            for object_tag_name in tag.to_name:
                if object_tag_name not in objects:
                    logger.info(
                        f'to_name={object_tag_name} is specified for output tag name={name}, '
                        'but we can\'t find it among input tags'
                    )
                    continue
                
                inputs.append(objects[object_tag_name])

            tag.set_objects(inputs)
            tag.set_labels(list(labels[name]))
            tag.set_labels_attrs(labels[name])

        return controls

    def _get_tag(self, name, tag_store):
        """
        """
        if name is not None:
            if name not in tag_store:
                raise Exception(f"Name {name} is not found, available names: {tag_store.keys()}")
            else:
                return tag_store[name]
        
        if tag_store and len(tag_store.keys()) > 1:
            raise Exception("Multiple object tags connected, you should specify name")
        
        return list(tag_store.values())[0]

    def get_tag(self, name):
        """
        """
        if name in self._controls:
            return self._controls[name]

        if name in self._objects:
            return self._objects[name]

        raise Exception(f"Tag with name {name} not found")
    
    def get_object(self, name=None):
        """
        """
        return self._get_tag(name, self._objects)
    
    def get_output(self, name=None):
        """Alias for below
        """
        return self.get_control(name)
    
    def get_control(self, name=None):
        """Returns the control tag that control tag maps to
        """
        return self._get_tag(name, self._controls)

    def find_tags_by_class(self, tag_class) -> List:
        """Find tags by tag type
        """
        lst = list(self.objects) + list(self.controls)
        tag_classes = [tag_class] if not isinstance(tag_class, list) else tag_class
        
        return [tag for tag in lst for cls in tag_classes if isinstance(tag, cls)]            
        
    def find_tags(self, tag_type: Optional[str] = None,
                  match_fn: Optional[Callable] = None) -> List:
        """Find tags that match_fn in entire parsed tree
        """
        tag_types = {
            'objects': self.objects,
            'controls': self.controls,
            # aliases
            'inputs': self.objects,
            'outputs': self.controls,
        }
        
        lst = tag_types.get(tag_type,
                            list(self.objects) + list(self.controls))
        
        if match_fn is not None:
            lst = list(filter(match_fn, lst))
        
        return lst    
    
    def parse(self, config_string: str) -> Tuple[Dict, Dict, Dict, etree._Element]:
        """Parses the received configuration string into dictionaries
        of ControlTags, ObjectTags, and Labels, along with an XML tree
        of the configuration.

        Args:
            config_string (str): the configuration string to be parsed.

        Returns:
            Tuple of:
            - Dictionary where keys are control tag names and values are ControlTag instances.
            - Dictionary where keys are object tag names and values are ObjectTag instances.
            - Dictionary of dictionaries where primary keys are label parent names 
              and secondary keys are label values and values are LabelTag instances.
            - An XML tree of the configuration.
        """
        try:
            xml_tree = etree.fromstring(config_string)
        except etree.XMLSyntaxError as e:
            raise LabelStudioXMLSyntaxErrorSentryIgnored(str(e))
        
        objects, controls, labels = {}, {}, defaultdict(dict)

        variables = []

        for tag in xml_tree.iter():
            if tag.attrib and 'indexFlag' in tag.attrib:
                variables.append(tag.attrib['indexFlag'])

            if ControlTag.validate_node(tag):
                controls[tag.attrib['name']] = ControlTag.parse_node(tag)
                
            elif ObjectTag.validate_node(tag):
                objects[tag.attrib['name']] = ObjectTag.parse_node(tag)

            elif LabelTag.validate_node(tag):
                lb = LabelTag.parse_node(tag, controls)
                labels[lb.parent_name][lb.value] = lb
                        
        return controls, objects, labels, xml_tree

    @classmethod
    def parse_config_to_json(cls, config_string):
        """
        """
        try:
            xml = etree.fromstring(config_string)
        except TypeError:
            raise etree.ParseError('can only parse strings')
        if xml is None:
            raise etree.ParseError('xml is empty or incorrect')

        config = xmljson.badgerfish.data(xml)
        config = _fix_choices(config)

        return config
    
    def _schema_validation(self, config_string):
        """
        """
        try:
            config = LabelingConfig.parse_config_to_json(config_string)
            jsonschema.validate(config, _LABEL_CONFIG_SCHEMA_DATA)
        except (etree.ParseError, ValueError) as exc:
            raise LabelStudioValidationErrorSentryIgnored(str(exc))
        except jsonschema.exceptions.ValidationError as exc:
            error_message = exc.context[-1].message if len(exc.context) else exc.message
            error_message = 'Validation failed on {}: {}'.format(
                '/'.join(map(str, exc.path)), error_message.replace('@', '')
            )
            raise LabelStudioValidationErrorSentryIgnored(error_message)
    
    def _to_name_validation(self, config_string):
        """
        """
        # toName points to existent name
        all_names = re.findall(r'name="([^"]*)"', config_string)
        
        names = set(all_names)
        toNames = re.findall(r'toName="([^"]*)"', config_string)
        for toName_ in toNames:
            for toName in toName_.split(','):
                if toName not in names:
                    raise LabelStudioValidationErrorSentryIgnored(f'toName="{toName}" not found in names: {sorted(names)}')
    
    def _unique_names_validation(self, config_string):
        """
        """
        # unique names in config # FIXME: 'name =' (with spaces) won't work
        all_names = re.findall(r'name="([^"]*)"', config_string)
        if len(set(all_names)) != len(all_names):
            raise LabelStudioValidationErrorSentryIgnored('Label config contains non-unique names')
    
    def validate(self):
        """
        """
        config_string = self._config
        
        # self._schema_validation(config_string)
        self._unique_names_validation(config_string)
        self._to_name_validation(config_string)

    @property
    def is_valid(self):
        """
        """
        try:
            self.validate()
            return True
        except LabelStudioValidationErrorSentryIgnored:
            return False
        
    @classmethod
    def validate_with_data(cls, config):
        """        
        """
        raise NotImplemented()
    
    def load_task(self, task):
        """When you load the task, it would replace the value in each
        object tag with actual data found in task. It returns a copy
        of the LabelConfig object

        """
        tree = copy.deepcopy(self)
        for obj in tree.objects:
            if obj.value_is_variable and obj.value_name in task:
                obj.value = task.get(obj.value_name)
        
        return tree
                
    def validate_task(self, task: "TaskValue", validate_regions_only=False):
        """
        """
        # TODO this might not be always true, and we need to use
        # "strict" param above to be able to configure

        # for every object tag we've got that has value as it's
        # variable we need to have an associated item in the task data
        for obj in self.objects:
            if obj.value_is_variable and \
               task["data"].get(obj.value_name, None) is None:
                return False
        
        if "annotations" in task and \
           not self.validate_annotation():
            return False
        
        if "predictions" in task and \
           not self.validate_prediction():
            return False

        return True
        
    def validate_annotation(self, annotation: "AnnotationValue"):
        """Given the annotation, match it to the config and return
        False if it's not valid

        """
        return all(self.validate_region(r) for r in annotation.get(RESULT_KEY))
        
        
    def validate_prediction(self, prediction: "PredictionValue"):
        """
        """
        return all(self.validate_region(r) for r in prediction.get(RESULT_KEY))
        
        
    def validate_region(self, region) -> bool:
        """
        """
        control = self.get_control(region["from_name"])
        obj = self.get_object(region["to_name"])

        # we should have both items present in the labeling config
        if not control or not obj:
            return False

        # type of the region should match the tag name
        if control.tag.lower() != region["type"]:
            return False

        # make sure that in config it connects to the same tag as
        # immplied by the region data
        if region["to_name"] not in control.to_name:
            return False

        # validate the actual value, for example that <Labels /> tag
        # is producing start, end, and labels
        if not control.validate_value(region["value"]):
            return False

        return True
        
    ### Generation

    def _sample_task(self, secure_mode=False):
        """
        """
        # predefined_task, annotations, predictions = get_task_from_labeling_config(label_config)
        generated_task = self.generate_sample_task(mode='editor_preview', secure_mode=secure_mode)
        
        if self._sample_config_task is not None:
            generated_task.update(self._sample_config_task)
        
        return generated_task, self._sample_config_ann, self._sample_config_pred

    
    def generate_sample_task(self, mode='upload', secure_mode=False):
        """This function generates a sample task based on the mode and secure_mode specified.

        :param mode: mode of operation, defaults to 'upload'
        :type mode: str
        :param secure_mode: mode specifying security, defaults to False
        :type secure_mode: bool
        :return: a dictionary representing the sample task
        :rtype: dict
        """
        task = {obj.value_name: obj.generate_example_value(mode=mode, secure_mode=secure_mode)
                for obj in self.objects}
        
        return task        
    
    def generate_sample_annotation(self):
        """
        """
        raise NotImplemented()

    #####
    ##### COMPATIBILITY LAYER
    #####
        
    def config_essential_data_has_changed(self, new_config_str):
        """Detect essential changes of the labeling config"""
        new_obj = LabelingConfig(config=new_config_str)
        
        for new_tag_name, new_tag in new_obj._controls.items():
            if new_tag_name not in self._controls:
                return True

            old_tag = self._controls[new_tag_name]
            
            if new_tag.tag != old_tag.tag:
                return True
            if new_tag.objects != old_tag.objects:
                return True
            if not set(old_tag.labels).issubset(new_tag.labels):
                return True

        return False

    
    def generate_sample_task_without_check(label_config, mode='upload', secure_mode=False):
        """
        """
        
    @classmethod
    def get_task_from_labeling_config(cls, config):
        """Get task, annotations and predictions from labeling config comment,
        it must start from "<!-- {" and end as "} -->"
        """
        # try to get task data, annotations & predictions from config comment
        task_data, annotations, predictions = {}, None, None
        start = config.find('<!-- {')
        start = start if start >= 0 else config.find('<!--{')
        start += 4
        end = config[start:].find('-->') if start >= 0 else -1

        if 3 < start < start + end:
            try:
                # logger.debug('Parse ' + config[start : start + end])
                body = json.loads(config[start : start + end])
            except Exception:
                # logger.error("Can't parse task from labeling config", exc_info=True)
                pass
            else:
                # logger.debug(json.dumps(body, indent=2))
                dont_use_root = 'predictions' in body or 'annotations' in body
                task_data = body['data'] if 'data' in body else (None if dont_use_root else body)
                predictions = body['predictions'] if 'predictions' in body else None
                annotations = body['annotations'] if 'annotations' in body else None
        
        return task_data, annotations, predictions
    
    @classmethod
    def config_line_stipped(self, c):
        tree = etree.fromstring(c, forbid_dtd=False)
        comments = tree.xpath('//comment()')

        for c in comments:
            p = c.getparent()
            if p is not None:
                p.remove(c)
            c = etree.tostring(tree, method='html').decode('utf-8')
        
        return c.replace('\n', '').replace('\r', '')

    
    def get_all_control_tag_tuples(label_config):
        """ """
        return [ tag.as_tuple() for tag in self.controls ]
        # outputs = parse_config(label_config)
        # out = []
        # for control_name, info in outputs.items():
        #     out.append(get_annotation_tuple(control_name, info['to_name'], info['type']))
        # return out
        
    def get_first_tag_occurence(
        self,
        control_type: Union[str, Tuple],
        object_type: Union[str, Tuple],
        name_filter: Optional[Callable] = None,
        to_name_filter: Optional[Callable] = None
    ) -> Tuple[str, str, str]:
        """
        Reads config and fetches the first control tag along with first object tag that matches the type.

        Args:
          control_type (str or tuple): The control type for checking tag matches.
          object_type (str or tuple): The object type for checking tag matches.
          name_filter (function, optional): If given, only tags with this name will be considered.
                                           Default is None.
          to_name_filter (function, optional): If given, only tags with this name will be considered.
                                              Default is None.

        Returns:
          tuple: (from_name, to_name, value), representing control tag, object tag and input value.        
        """
        
        for tag in self._objects.values():
            if tag.match(control_type, name_filter_fn=name_filter):
                for object_tag in tag.objects:
                    if object_tag.match(object_type, to_name_filter_fn=to_name_filter):
                        return tag.name, object_tag.name, object_tag.value
                    
        raise ValueError(f'No control tag of type {control_type} and object tag of type {object_type} found in label config')

    def get_all_labels(self):
        """
        """
        dynamic_values = {c.name: True for c in self.controls if c.dynamic_value}
        return self._labels, dynamic_values

    def get_all_object_tag_names(self):
        """
        """
        return set(self.extract_data_types)
    
    def extract_data_types(self):
        """
        """
        # label_config = self._config
        # xml = etree.fromstring(label_config, forbid_dtd=False)
        # if xml is None:
        #     raise etree.ParseError('Project config is empty or incorrect')

        # TODO check if not implementing that regex match is an issue
        data_type = {}
        value_tags = self.find_tags(match_fn=lambda tag: bool(tag.name and tag.value))
        
        for tag in value_tags:
            value = tag.value
            if data_type.get(value) != 'Video':
                data_type[value] = tag.tag

        return data_type
    
        # take all tags with values attribute and fit them to tag types
        # data_type = {}
        # parent = xml.findall('.//*[@value]')
        # for match in parent:
        #     if not match.get('name'):
        #         continue
        #     name = match.get('value')

        #     # simple one
        #     if len(name) > 1 and (name[0] == '$'):
        #         name = name[1:]
        #         # video has highest priority, e.g.
        #         # for <Video value="url"/> <Audio value="url"> it must be data_type[url] = Video
        #         if data_type.get(name) != 'Video':
        #             data_type[name] = match.tag

                    
        #     # regex
        #     else:
        #         pattern = r'\$\w+'  # simple one: r'\$\w+'
        #         regex = re.findall(pattern, name)
        #         first = regex[0][1:] if len(regex) > 0 else ''

        #         if first:
        #             if data_type.get(first) != 'Video':
        #                 data_type[first] = match.tag

        # return data_type

    
    ##### OLD API 
        
    
        # for component in parsed_config:
        #     if parsed_config[component]['type'].lower() in _VIDEO_TRACKING_TAGS:
        #         return True


    # def extract_data_types(self):
    #     """
    #     """
    #     label_config = self._config
    #     xml = etree.fromstring(label_config, forbid_dtd=False)
    #     if xml is None:
    #         raise etree.ParseError('Project config is empty or incorrect')

    #     # take all tags with values attribute and fit them to tag types
    #     data_type = {}
    #     parent = xml.findall('.//*[@value]')
    #     for match in parent:
    #         if not match.get('name'):
    #             continue
    #         name = match.get('value')

    #         # simple one
    #         if len(name) > 1 and (name[0] == '$'):
    #             name = name[1:]
    #             # video has highest priority, e.g.
    #             # for <Video value="url"/> <Audio value="url"> it must be data_type[url] = Video
    #             if data_type.get(name) != 'Video':
    #                 data_type[name] = match.tag

    #         # regex
    #         else:
    #             pattern = r'\$\w+'  # simple one: r'\$\w+'
    #             regex = re.findall(pattern, name)
    #             first = regex[0][1:] if len(regex) > 0 else ''

    #             if first:
    #                 if data_type.get(first) != 'Video':
    #                     data_type[first] = match.tag

    #     return data_type

    def is_video_object_tracking(parsed_config):
        """
        """
        match_fn = lambda tag: tag in _VIDEO_TRACKING_TAGS
        return bool(self.find_tags(match_fn=match_fn))
        
    def is_type(self, tag_type=None):
        """
        """

    def validate_label_config(self, config_string):
        # xml and schema
        self._schema_validation(config_string)
        self._unique_names_validation(config_string)
        self._to_name_validation(config_string)
        

    @classmethod
    def validate_config_using_summary(self, summary, strict=False):
        """Validate current config using LS Project Summary
        """
        # this is a rewrite of project.validate_config function
        # self.validate_label_config(config_string)
        if not self._objects:
            return False
        
        created_labels = summary.created_labels
        created_labels_drafts = summary.created_labels_drafts
        annotations_summary = summary.created_annotations
        
        self.validate_annotations_consistency(annotations_summary)
        self.validate_lables_consistency(created_labels, created_labels_drafts)    

    def validate_lables_consistency(self, created_labels, created_labels_drafts):
        """
        """
        # validate labels consistency
        # labels_from_config, dynamic_values_tags = self.get_all_labels(config_string)
        
        created_labels = merge_labels_counters(created_labels, created_labels_drafts)

        # <Labels name="sentinement" ...><Label value="Negative" ... />
        # {'sentiment': {'Negative': 1, 'Positive': 3, 'Neutral': 1}}
        
        for control_tag_from_data, labels_from_data in created_labels.items():
            # Check if labels created in annotations, and their control tag has been removed
            control_from_config = self.get_object(control_tag_from_data)
            
            if labels_from_data and not self.get_object(control_tag_from_data):
                raise LabelStudioValidationErrorSentryIgnored(
                    f'There are {sum(labels_from_data.values(), 0)} annotation(s) created with tag '
                    f'"{control_tag_from_data}", you can\'t remove it'
                )

            removed_labels = []
            # Check that labels themselves were not removed
            for label_name, label_value in labels_from_data.items:
                if label_value > 0 and \
                   not control_from_config.label_attrs.get(label_name, None):
                    # that label was used in labeling before, but not
                    # present in the current config
                    removed_labels.append(label_name)

            # TODO that needs to be added back
            # if 'VideoRectangle' in tag_types:
            #     for key in labels_from_config:
            #         labels_from_config_by_tag |= set(labels_from_config[key])

            # if 'Taxonomy' in tag_types:
            #     custom_tags = Label.objects.filter(links__project=self).values_list('value', flat=True)
            #     flat_custom_tags = set([item for sublist in custom_tags for item in sublist])
            #     labels_from_config_by_tag |= flat_custom_tags
                    
            if len(removed_labels):
                raise LabelStudioValidationErrorSentryIgnored(
                    f'These labels still exist in annotations or drafts:\n{",".join(removed_labels)}'
                    f'Please add labels to tag with name="{str(control_tag_from_data)}".'
                )        

    def validate_annotations_consistency(self, annotations_summary):
        """
        """
        # annotations_summary is coming from LS Project Summary, it's
        # format is: { "chc|text|choices": 10 }
        # which means that there are two tags, Choices, and one of
        # object tags and there are 10 annotations
        
        err = []
        annotations_from_data = set(annotations_summary)
        
        for ann in annotations_from_data:
            from_name, to_name, tag_type = ann.split("|")

            # avoid textarea to_name check (see DEV-1598)
            if tag_type.lower() == 'textarea':
                continue
            
            control = self.get_control(from_name)
            if not control or not control.get_object(to_name):
                err.append(f'with from_name={from_name}, to_name={to_name}, type={tag_type}')

        if err:
            diff_str = '\n'.join(err)
            raise LabelStudioValidationErrorSentryIgnored(
                f'Created annotations are incompatible with provided labeling schema, we found:\n{diff_str}')        

    
