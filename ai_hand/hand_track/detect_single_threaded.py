import datetime

import cv2

from ai_hand.hand_track.utils import detector_utils

detection_graph, sess = detector_utils.load_inference_graph()

if __name__ == '__main__':

    cap = cv2.VideoCapture(1)

    start_time = datetime.datetime.now()
    num_frames = 0
    im_width, im_height = (cap.get(3), cap.get(4))
    # max number of hands we want to detect/track
    num_hands_detect = 1

    cv2.namedWindow('Single-Threaded Detection', cv2.WINDOW_NORMAL)

    while True:
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        ret, image_np = cap.read()
        # image_np = cv2.flip(image_np, 1)
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        # Actual detection. Variable boxes contains the bounding box cordinates for hands detected,
        # while scores contains the confidence for each of these boxes.
        # Hint: If len(boxes) > 1 , you may assume you have found atleast one hand (within your score threshold)
        boxes, scores = detector_utils.detect_objects(image_np,
                                                      detection_graph, sess)

        # draw bounding boxes on frame
        for box, score in zip(boxes, scores):
            if score > 0.8:
                top_left = (int(box[1] * 640), int(box[0]*480))
                bottom_right = (int(box[3] * 640), int(box[2]*480))
                cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 4)
                cv2.putText(image_np, f"Score: {score}", bottom_right, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

        # Calculate Frames per second (FPS)
        num_frames += 1
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = num_frames / elapsed_time


        # Display FPS on frame
        detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                            image_np)

        cv2.imshow('Single-Threaded Detection',
                    cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
