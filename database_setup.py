# configuration
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

#  class for the table 
class Restaurant(Base):
    # table info
    __tablename__ = 'restaurant'
    #mappers
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    menuitems = relationship('MenuItem',cascade="all, delete")  #single_parent=True 
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name
            }

    
 #  class object for the table
class MenuItem(Base):
    # table info
    __tablename__ = 'menu_item'
    #maper info for colmu
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id')) #,ondelete='CASCADE'
    #restaurant = relationship(Restaurant,cascade="all, delete")  #single_parent=True 
 
    @property
    def serialize(self):
        # return object in serialized format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course,
        }
        
# configuyration info
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)