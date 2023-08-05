# -*- coding: utf-8 -*-

"""
    api_tester_upload_test

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

from api_tester_upload_test.api_helper import APIHelper

class UnixDateTime(object):

    """Implementation of the 'Unix DateTime' model.

    TODO: type model description here.

    Attributes:
        date_time (datetime): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "date_time":'dateTime'
    }

    def __init__(self,
                 date_time=None,
                 additional_properties = {}):
        """Constructor for the UnixDateTime class"""

        # Initialize members of the class
        self.date_time = APIHelper.UnixDateTime(date_time) if date_time else None

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
        date_time = APIHelper.UnixDateTime.from_value(dictionary.get("dateTime")).datetime if dictionary.get("dateTime") else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(date_time,
                   dictionary)


