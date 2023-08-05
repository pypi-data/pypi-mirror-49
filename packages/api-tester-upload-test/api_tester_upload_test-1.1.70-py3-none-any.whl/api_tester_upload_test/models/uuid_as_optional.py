# -*- coding: utf-8 -*-

"""
    api_tester_upload_test

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""


class UuidAsOptional(object):

    """Implementation of the 'uuid as optional' model.

    TODO: type model description here.

    Attributes:
        uuid (uuid|string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "uuid":'uuid'
    }

    def __init__(self,
                 uuid=None,
                 additional_properties = {}):
        """Constructor for the UuidAsOptional class"""

        # Initialize members of the class
        self.uuid = uuid

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
        uuid = dictionary.get('uuid')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(uuid,
                   dictionary)


