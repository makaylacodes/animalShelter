#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 19:56:46 2023

@author: makaylaanders_snhu
"""
from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'localhost'
        PORT = 27017
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            self.database.animals.insert_one(data) # data should be dictionary            
            return True
        return False

# Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None:
            readData = self.database.animals.find(query)  # data should be dictionary            
            return readData
        else:
            return []

# Create method to implement the U in CRUD.
    def update(self, query, updatedDoc):
        if query is not None:
            # data should be dictionary            
            updatedData = self.database.animals.update_one(query, {"$set": updatedDoc}) 
            return updatedData.modified_count
        else:
            return []

# Create method to implement the D in CRUD.
    def delete(self, query):
        if query is not None:
            # data should be dictionary  
            toBeDeleted = self.database.animals.delete_one(query)            
            return toBeDeleted.deleted_count
        else:
            return []