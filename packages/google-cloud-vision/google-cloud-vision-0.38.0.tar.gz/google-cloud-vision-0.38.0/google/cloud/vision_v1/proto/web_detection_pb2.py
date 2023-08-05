# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/vision_v1/proto/web_detection.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/cloud/vision_v1/proto/web_detection.proto",
    package="google.cloud.vision.v1",
    syntax="proto3",
    serialized_options=_b(
        "\n\032com.google.cloud.vision.v1B\021WebDetectionProtoP\001Z<google.golang.org/genproto/googleapis/cloud/vision/v1;vision\370\001\001\242\002\004GCVN"
    ),
    serialized_pb=_b(
        '\n0google/cloud/vision_v1/proto/web_detection.proto\x12\x16google.cloud.vision.v1\x1a\x1cgoogle/api/annotations.proto"\xd4\x06\n\x0cWebDetection\x12\x44\n\x0cweb_entities\x18\x01 \x03(\x0b\x32..google.cloud.vision.v1.WebDetection.WebEntity\x12K\n\x14\x66ull_matching_images\x18\x02 \x03(\x0b\x32-.google.cloud.vision.v1.WebDetection.WebImage\x12N\n\x17partial_matching_images\x18\x03 \x03(\x0b\x32-.google.cloud.vision.v1.WebDetection.WebImage\x12P\n\x1apages_with_matching_images\x18\x04 \x03(\x0b\x32,.google.cloud.vision.v1.WebDetection.WebPage\x12N\n\x17visually_similar_images\x18\x06 \x03(\x0b\x32-.google.cloud.vision.v1.WebDetection.WebImage\x12H\n\x11\x62\x65st_guess_labels\x18\x08 \x03(\x0b\x32-.google.cloud.vision.v1.WebDetection.WebLabel\x1a\x42\n\tWebEntity\x12\x11\n\tentity_id\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\x02\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x1a&\n\x08WebImage\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\x02\x1a\x30\n\x08WebLabel\x12\r\n\x05label\x18\x01 \x01(\t\x12\x15\n\rlanguage_code\x18\x02 \x01(\t\x1a\xd6\x01\n\x07WebPage\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\r\n\x05score\x18\x02 \x01(\x02\x12\x12\n\npage_title\x18\x03 \x01(\t\x12K\n\x14\x66ull_matching_images\x18\x04 \x03(\x0b\x32-.google.cloud.vision.v1.WebDetection.WebImage\x12N\n\x17partial_matching_images\x18\x05 \x03(\x0b\x32-.google.cloud.vision.v1.WebDetection.WebImageBy\n\x1a\x63om.google.cloud.vision.v1B\x11WebDetectionProtoP\x01Z<google.golang.org/genproto/googleapis/cloud/vision/v1;vision\xf8\x01\x01\xa2\x02\x04GCVNb\x06proto3'
    ),
    dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR],
)


_WEBDETECTION_WEBENTITY = _descriptor.Descriptor(
    name="WebEntity",
    full_name="google.cloud.vision.v1.WebDetection.WebEntity",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="entity_id",
            full_name="google.cloud.vision.v1.WebDetection.WebEntity.entity_id",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="score",
            full_name="google.cloud.vision.v1.WebDetection.WebEntity.score",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="description",
            full_name="google.cloud.vision.v1.WebDetection.WebEntity.description",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=586,
    serialized_end=652,
)

_WEBDETECTION_WEBIMAGE = _descriptor.Descriptor(
    name="WebImage",
    full_name="google.cloud.vision.v1.WebDetection.WebImage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="url",
            full_name="google.cloud.vision.v1.WebDetection.WebImage.url",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="score",
            full_name="google.cloud.vision.v1.WebDetection.WebImage.score",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=654,
    serialized_end=692,
)

_WEBDETECTION_WEBLABEL = _descriptor.Descriptor(
    name="WebLabel",
    full_name="google.cloud.vision.v1.WebDetection.WebLabel",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="label",
            full_name="google.cloud.vision.v1.WebDetection.WebLabel.label",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="language_code",
            full_name="google.cloud.vision.v1.WebDetection.WebLabel.language_code",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=694,
    serialized_end=742,
)

_WEBDETECTION_WEBPAGE = _descriptor.Descriptor(
    name="WebPage",
    full_name="google.cloud.vision.v1.WebDetection.WebPage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="url",
            full_name="google.cloud.vision.v1.WebDetection.WebPage.url",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="score",
            full_name="google.cloud.vision.v1.WebDetection.WebPage.score",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="page_title",
            full_name="google.cloud.vision.v1.WebDetection.WebPage.page_title",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="full_matching_images",
            full_name="google.cloud.vision.v1.WebDetection.WebPage.full_matching_images",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="partial_matching_images",
            full_name="google.cloud.vision.v1.WebDetection.WebPage.partial_matching_images",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=745,
    serialized_end=959,
)

_WEBDETECTION = _descriptor.Descriptor(
    name="WebDetection",
    full_name="google.cloud.vision.v1.WebDetection",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="web_entities",
            full_name="google.cloud.vision.v1.WebDetection.web_entities",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="full_matching_images",
            full_name="google.cloud.vision.v1.WebDetection.full_matching_images",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="partial_matching_images",
            full_name="google.cloud.vision.v1.WebDetection.partial_matching_images",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="pages_with_matching_images",
            full_name="google.cloud.vision.v1.WebDetection.pages_with_matching_images",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="visually_similar_images",
            full_name="google.cloud.vision.v1.WebDetection.visually_similar_images",
            index=4,
            number=6,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="best_guess_labels",
            full_name="google.cloud.vision.v1.WebDetection.best_guess_labels",
            index=5,
            number=8,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[
        _WEBDETECTION_WEBENTITY,
        _WEBDETECTION_WEBIMAGE,
        _WEBDETECTION_WEBLABEL,
        _WEBDETECTION_WEBPAGE,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=107,
    serialized_end=959,
)

_WEBDETECTION_WEBENTITY.containing_type = _WEBDETECTION
_WEBDETECTION_WEBIMAGE.containing_type = _WEBDETECTION
_WEBDETECTION_WEBLABEL.containing_type = _WEBDETECTION
_WEBDETECTION_WEBPAGE.fields_by_name[
    "full_matching_images"
].message_type = _WEBDETECTION_WEBIMAGE
_WEBDETECTION_WEBPAGE.fields_by_name[
    "partial_matching_images"
].message_type = _WEBDETECTION_WEBIMAGE
_WEBDETECTION_WEBPAGE.containing_type = _WEBDETECTION
_WEBDETECTION.fields_by_name["web_entities"].message_type = _WEBDETECTION_WEBENTITY
_WEBDETECTION.fields_by_name[
    "full_matching_images"
].message_type = _WEBDETECTION_WEBIMAGE
_WEBDETECTION.fields_by_name[
    "partial_matching_images"
].message_type = _WEBDETECTION_WEBIMAGE
_WEBDETECTION.fields_by_name[
    "pages_with_matching_images"
].message_type = _WEBDETECTION_WEBPAGE
_WEBDETECTION.fields_by_name[
    "visually_similar_images"
].message_type = _WEBDETECTION_WEBIMAGE
_WEBDETECTION.fields_by_name["best_guess_labels"].message_type = _WEBDETECTION_WEBLABEL
DESCRIPTOR.message_types_by_name["WebDetection"] = _WEBDETECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WebDetection = _reflection.GeneratedProtocolMessageType(
    "WebDetection",
    (_message.Message,),
    dict(
        WebEntity=_reflection.GeneratedProtocolMessageType(
            "WebEntity",
            (_message.Message,),
            dict(
                DESCRIPTOR=_WEBDETECTION_WEBENTITY,
                __module__="google.cloud.vision_v1.proto.web_detection_pb2",
                __doc__="""Entity deduced from similar images on the Internet.
    
    
    Attributes:
        entity_id:
            Opaque entity ID.
        score:
            Overall relevancy score for the entity. Not normalized and not
            comparable across different image queries.
        description:
            Canonical description of the entity, in English.
    """,
                # @@protoc_insertion_point(class_scope:google.cloud.vision.v1.WebDetection.WebEntity)
            ),
        ),
        WebImage=_reflection.GeneratedProtocolMessageType(
            "WebImage",
            (_message.Message,),
            dict(
                DESCRIPTOR=_WEBDETECTION_WEBIMAGE,
                __module__="google.cloud.vision_v1.proto.web_detection_pb2",
                __doc__="""Metadata for online images.
    
    
    Attributes:
        url:
            The result image URL.
        score:
            (Deprecated) Overall relevancy score for the image.
    """,
                # @@protoc_insertion_point(class_scope:google.cloud.vision.v1.WebDetection.WebImage)
            ),
        ),
        WebLabel=_reflection.GeneratedProtocolMessageType(
            "WebLabel",
            (_message.Message,),
            dict(
                DESCRIPTOR=_WEBDETECTION_WEBLABEL,
                __module__="google.cloud.vision_v1.proto.web_detection_pb2",
                __doc__="""Label to provide extra metadata for the web detection.
    
    
    Attributes:
        label:
            Label for extra metadata.
        language_code:
            The BCP-47 language code for ``label``, such as "en-US" or
            "sr-Latn". For more information, see http://www.unicode.org/re
            ports/tr35/#Unicode\_locale\_identifier.
    """,
                # @@protoc_insertion_point(class_scope:google.cloud.vision.v1.WebDetection.WebLabel)
            ),
        ),
        WebPage=_reflection.GeneratedProtocolMessageType(
            "WebPage",
            (_message.Message,),
            dict(
                DESCRIPTOR=_WEBDETECTION_WEBPAGE,
                __module__="google.cloud.vision_v1.proto.web_detection_pb2",
                __doc__="""Metadata for web pages.
    
    
    Attributes:
        url:
            The result web page URL.
        score:
            (Deprecated) Overall relevancy score for the web page.
        page_title:
            Title for the web page, may contain HTML markups.
        full_matching_images:
            Fully matching images on the page. Can include resized copies
            of the query image.
        partial_matching_images:
            Partial matching images on the page. Those images are similar
            enough to share some key-point features. For example an
            original image will likely have partial matching for its
            crops.
    """,
                # @@protoc_insertion_point(class_scope:google.cloud.vision.v1.WebDetection.WebPage)
            ),
        ),
        DESCRIPTOR=_WEBDETECTION,
        __module__="google.cloud.vision_v1.proto.web_detection_pb2",
        __doc__="""Relevant information for the image from the Internet.
  
  
  Attributes:
      web_entities:
          Deduced entities from similar images on the Internet.
      full_matching_images:
          Fully matching images from the Internet. Can include resized
          copies of the query image.
      partial_matching_images:
          Partial matching images from the Internet. Those images are
          similar enough to share some key-point features. For example
          an original image will likely have partial matching for its
          crops.
      pages_with_matching_images:
          Web pages containing the matching images from the Internet.
      visually_similar_images:
          The visually similar image results.
      best_guess_labels:
          The service's best guess as to the topic of the request image.
          Inferred from similar images on the open web.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.vision.v1.WebDetection)
    ),
)
_sym_db.RegisterMessage(WebDetection)
_sym_db.RegisterMessage(WebDetection.WebEntity)
_sym_db.RegisterMessage(WebDetection.WebImage)
_sym_db.RegisterMessage(WebDetection.WebLabel)
_sym_db.RegisterMessage(WebDetection.WebPage)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
