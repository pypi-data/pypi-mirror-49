# preprocess: 

This package contains preprocessing functions for the Open Image Dataset.
1.	CheckFile.py: contains functions to verify the correctness of the data.
2.	CreateTables.py: contains functions to create all tables(bounding box table, category table, image tables).
3.	SaveClassInfo.py: contains functions related to the classes.
4.	TestPerformance.py: contains functions to test the current tables.
5.	UpdateImageInfo.py: contains functions to merge the image and bounding box informations into current tables.
6.	The schemas of all tables is shown below:

## bbox

|Column Name|Type|Description|
|----|:------:|:------:|
|     BoxID     | string |                  The unique id of the bounding box                   |
|    ImageID    | string |                      The unique id of the image                      |
|      XMin     |  int   |                        Coordinate of the box                         |
|      XMax     |  int   |                        Coordinate of the box                         |
|      YMin     |  int   |                        Coordinate of the box                         |
|      YMax     |  int   |                        Coordinate of the box                         |
|      Area     |  int   |                         The area of the box                          |
|   IsOccluded  |  int   | Indicates that the object is occluded by another object in the image |
|  IsTruncated  |  int   |  Indicates that the object extends beyond the boundary of the image  |
|   IsGroupOf   |  int   |           Indicates that the box spans a group of objects            |
|  IsDepiction  |  int   |               Indicates that the object is a depiction               |
|    IsInside   |  int   |       Indicates a picture taken from the inside of the object        |
| LuminanceMean |  int   |                    The luminance mean of the box                     |
|  LuminanceStd |  int   |                     The luminance std of the box                     |
|    Category   | string |                       The category of the box                        |

## category

|Column Name|Type|Description|
|----|:------:|:------:|
|   Category  | string |         The category of the bounding boxes        |
|  BoxIDList  | string | The bounding box ids that belong to this category |
| ImageIDList | string |     The image ids that belong to this category    |

## image-t1

|Column Name|Type|Description|
|----|:------:|:------:|
|      ImageID       | string |           The unique id of the image           |
|     BoxIDList      | string | The bounding box ids that belong to this image |
|  ImageQualityMean  |  int   |         The quality mean of the image          |
|  ImageQualityStd   |  int   |          The quality std of the image          |
|    CategoryList    | string |   The categories of the image(small to big)    |
|        Mode        | string |          The mode of the image(RGB,L)          |
|       Width        |  int   |             The width of the image             |
|       Height       |  int   |            The height of the image             |
| ImageLuminanceMean |  int   |        The luminance mean of the image         |
| ImageLuminanceStd  |  int   |         The luminance std of the image         |

## image-t2

|Column Name|Type|Description|
|----|:------:|:------:|
| NumofboundingBox |  int   |         The number of bounding boxes of the image         |
|   ImageIDList    | string | The image ids that have the same number of bounding boxes |

## image-t3

|Column Name|Type|Description|
|----|:------:|:------:|
|   ImageID   | string |   The unique id of the image  |
|     Url     | string | The download url of the image |


# sparkpreprocess: 
This package contains preprocessing function running on spark for the Open Image Dataset.
sparkpreprocess.py: contains functions to read image in azure blob, get image and bouding box information.
    1. sparkHadoopConf(): Use accountKey or sas tokens to access azure blob storage
    2. GetImageRdds(): Read images and return a list of rdds, each element of rdd contains the image's full path in azure blob and image object.
    3. GetBoxesLightness(): Get lightness of bounding boxes with an Image.
    4. GetImageInfo(img:Image): Get image information from image Object.
    5. SaveImageInfo(): Save image information at blob.