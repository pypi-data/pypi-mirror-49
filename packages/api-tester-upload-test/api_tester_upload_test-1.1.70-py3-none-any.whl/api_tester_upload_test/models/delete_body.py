# -*- coding: utf-8 -*-

"""
    api_tester_upload_test

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""


class DeleteBody(object):

    """Implementation of the 'delete_body' model.

    TODO: type model description here.

    Attributes:
        name (string): TODO: type description here.
        field (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "field":'field',
        "name":'name'
    }

    def __init__(self,
                 field=None,
                 name=None,
                 additional_properties = {}):
        """Constructor for the DeleteBody class"""

        # Initialize members of the class
        self.name = name
        self.field = field

        # Add additional model properties to the instance
        self.additional_properties = additional_properties


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        field = dictionary.get('field')
        name = dictionary.get('name')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(field,
                   name,
                   dictionary)


