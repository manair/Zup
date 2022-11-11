#from PIL import Image
import face_recognition
from localdata import  DBConn as db

def recogFace():
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file("images/img.png")

    # Find all the faces in the image using the default HOG-based model.
    # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
    # See also: find_faces_in_picture_cnn.py
    face_locations = face_recognition.face_locations(image)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))

    return face_locations

def encodefoundfaces(face):

    for face_location in face:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        unknownface = face_recognition.face_encodings(face_location)
        inserface = "insert into facecode (faceencoding, profileid, keyword) values ({},{},{});".format()
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                    right))
        db.myConn(inserface)


        # You can access the actual face itself like this:
        #face_image = image[top:bottom, left:right]
        # pil_image = Image.fromarray(face_image)
        # pil_image.show()

    return

def identifieface(encodedface):
    inserface = "select faceencoding, profileid, keyword) from facecode;"
    knownfc = db.myConn(inserface)
    return