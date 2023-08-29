import os
import requests
from bs4 import BeautifulSoup, Tag, ResultSet
from app.db.schemas import DataSetBase


source_domain:str = os.environ.get("SOURCE_DOMAIN")
source_url:str = os.environ.get("SOURCE_URL")
headers:dict[str,str] = {'Content-Type': 'text/html'}

class DataSet:
    """
    A dataset item class
    """
    def __init__(self, name, organization, description, link):
        """
        Constructor for a dataset item

        Args:
            name (str): The name of the dataset
            organization (str): The organization which published the dataset
            description (str): The description of the dataset contents
            link (str): The link to the dataset
        """
        self.name = name
        self.organization = organization
        self.description = description
        self.link = link
    
    def to_dict(self):
        """
        Convert the object attributes to a dictionary

        Returns:
            dict: A dictionary containing object attributes
        """
        return {
            "name": self.name,
            "organization": self.organization,
            "description": self.description,
            "link": self.link
        }
    
    def to_schema(self)-> DataSetBase:
        """
        Transform into a DataSetBase schema

        Returns:
            db.schemas: A database schema DataSet model
        """
        model = DataSetBase(
            name=self.name,
            organization=self.organization,
            description=self.description,
            link=self.link
        )
            
        return model
        
        


def scrape(url:str, page_number:int)-> list[DataSet]:
    """
    Scrape a page, parse contents, and transform into a list of datasets

    Args:
        url (str): The url of the page to scrape
        page_number (int): The page number

    Returns:
        list[DataSet]: A list of tranformed datasets
    """
    
    if page_number is None:
        page_number = 1

    page:requests.Response = requests.get(url)
    soup:BeautifulSoup = BeautifulSoup(page.content, 'html.parser')
    datasets:list[DataSet] = transform_soup(soup)

    return datasets


def transform_soup(soup:BeautifulSoup) -> list[DataSet]:
    """
    Transform the soup into a list of datasets

    Args:
        soup (BeautifulSoup): The soup which contains parsed HTML

    Returns:
        list[DataSet]: A list of datasets after transformation
    """
    
    data_set_items:ResultSet[Tag] = soup.find_all("li", class_="dataset-item has-organization")
    datasets:list[DataSet] = []
    
    for item in data_set_items:
        datasets.append(transform_tag_item(item))
        
    return datasets

def transform_tag_item(item:Tag) -> DataSet:
    """
    Transform the tag item which contains dataset as HTML into a dataset

    Args:
        item (Tag): The tag item which contains partial of the parsed HTML

    Returns:
        DataSet: A dataset after transformation
    """
    
    name:str = find_dataset_name(item)
    organization:str = find_dataset_organization(item)
    description:str = find_dataset_description(item)
    link:str = find_dataset_link(item)
    
    dataset = DataSet(name, organization, description, link)
    
    return dataset

def find_dataset_name(item:Tag)->str:
    """
    Find the dataset name in a tag item

    Args:
        item (Tag): The tag item which contains partial of the parsed HTML

    Returns:
        str: The dataset name
    """
    
    heading:Tag = item.find("h3", class_="dataset-heading")
    name:str = heading.find("a").text
        
    return name

def find_dataset_organization(item:Tag)->str:
    """
    Find the dataset organization in a tag item

    Args:
        item (Tag): The tag item which contains partial of the parsed HTML

    Returns:
        str: The dataset organization
    """
    
    notes:Tag = item.find("div", class_="notes")
    org:str = notes.find("p", class_="dataset-organization").text
    
    if org.endswith("—"):
        org = org[:-2]
        org = org.strip()
    
    return org


def find_dataset_description(item:Tag)->str:
    """
    Find the dataset description in a tag item
    
    Args:
        item (Tag): The tag item which contains partial of the parsed HTML

    Returns:
        str: The dataset description
    """
    
    notes:Tag = item.find("div", class_="notes")
    desc:str = notes.find("div").text
        
    return desc



def find_dataset_link(item:Tag)->str:
    """
    Find the dataset link in a tag item
    
    Args:
        item (Tag): The tag item which contains partial of the parsed HTML

    Returns:
        str: The dataset link
    """
    heading:Tag = item.find("h3", class_="dataset-heading")
    href:str = heading.find("a").attrs['href']
    link:str = source_domain + href
    
    return link


def get_scraped_data()->list[DataSet]:
    """
    Get scraped data

    Returns:
        list[DataSet]: A list of transformed datasets
    
    """
    
    data = scrape(source_url, None)
    return data