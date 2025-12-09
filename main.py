import cv2


def motion_detection(cam):
    # set video source and error check
    cap = cv2.VideoCapture(cam)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # get the video frames' width and height for proper saving of videos
    # where 3, 4 and CAP_PROP_FPS are propIDs to get certain informations about a video stream
    # check https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    if (
        fps == 0.0
    ):  # video stream may sometimes return no fps value in which case we assume it to be 30
        fps = 30.0

    frame_size = (frame_width, frame_height)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_video = "recorded.mp4"

    # create the `VideoWriter()` object
    out = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    # Create Background Subtractor MOG2 object
    backSub = cv2.createBackgroundSubtractorMOG2()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            # Apply background subtraction
            fg_mask = backSub.apply(frame)

            # apply global threshol to remove shadows
            retval, mask_thresh = cv2.threshold(fg_mask, 180, 255, cv2.THRESH_BINARY)

            # set the kernal
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            # Apply erosion
            mask_eroded = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)

            # Find contours
            contours, hierarchy = cv2.findContours(
                mask_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            min_contour_area = 500  # minimum area to consider for movement
            # filtering
            large_contours = [
                cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area
            ]
            frame_out = frame.copy()

            # check if any big changes are detect, only then save  and draw
            if (
                len(large_contours) > 0
            ):  # this simple check allows for only writing when there is some movement
                # TODO: add timer after detected movement
                # TODO: add current time at corner of screen
                # TODO: add 10second buffer for previous frames before movement
                for cnt in large_contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    frame_out = cv2.rectangle(
                        frame, (x, y), (x + w, y + h), (0, 0, 200), 3
                    )

                out.write(frame_out)
            # saving the video file

            # Display the resulting frame
            cv2.imshow("Frame_final", frame_out)

            # Press Q on keyboard to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    # When everything done, release the video capture and writer object
    cap.release()
    out.release()
    # Closes all the frames
    cv2.destroyAllWindows()


motion_detection(0)
