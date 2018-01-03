import time

from object_detection.vantara import lumada_stuff

dangerous_items = [49, #knife
				  87, #scissors
				   39, #baseball bat
                   44, #bottle
                   48 #fork
				  ]

dangerous_items_score = [100, #knife
                   60, #scissors
                   85, #baseball bat
                   10, #bottle
                    20 #fork
                   ]
def check_if_is_a_dangerous_object( image_obj, score ):
    s = set(dangerous_items)

    image_obj['danger']=0
    image_obj['timestamp']=time.time()
    image_obj['level'] = 0
	
    if image_obj ['id'] in s:
        idx = dangerous_items.index(image_obj ['id'])
        image_obj['danger']=1
        image_obj['level'] = dangerous_items_score[idx]

    register_dangerous_object_alert(image_obj)

def register_dangerous_object_alert( image_obj ):
    lumada_stuff.publish_state(image_obj)