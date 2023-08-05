# -*- coding: utf-8 -*-

"""
    api_tester_upload_test

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import api_tester_upload_test.models.gloss_div

class Glossary(object):

    """Implementation of the 'Glossary' model.

    TODO: type model description here.

    Attributes:
        title (string): TODO: type description here.
        gloss_div (GlossDiv): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "gloss_div":'GlossDiv',
        "title":'title'
    }

    def __init__(self,
                 gloss_div=None,
                 title=None,
                 additional_properties = {}):
        """Constructor for the Glossary class"""

        # Initialize members of the class
        self.title = title
        self.gloss_div = gloss_div

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
        gloss_div = api_tester_upload_test.models.gloss_div.GlossDiv.from_dictionary(dictionary.get('GlossDiv')) if dictionary.get('GlossDiv') else None
        title = dictionary.get('title')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(gloss_div,
                   title,
                   dictionary)


