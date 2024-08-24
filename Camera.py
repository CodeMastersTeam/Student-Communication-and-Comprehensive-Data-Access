import gi #type: ignore
import cv2
import numpy as np

gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import Gst, GstVideo #type: ignore
 
def main():
    Gst.init(None)

    pipeline = Gst.Pipeline()

    # Create elements
    src = Gst.ElementFactory.make("v4l2src", "video-source")
    video_convert = Gst.ElementFactory.make("videoconvert", "convert")
    caps = Gst.Caps.from_string("video/x-raw, format=BGR")
    video_convert.set_property("format", caps)  # Set the format property
    appsink = Gst.ElementFactory.make("appsink", "sink")

    # Add elements to pipeline
    pipeline.add(src)
    pipeline.add(video_convert)
    pipeline.add(appsink)

    # Link elements
    src.link(video_convert)
    video_convert.link(appsink)

    # Set up bus for messages
    bus = pipeline.get_bus()
    bus.add_signal_watch()

    def on_message(bus, message):
        if message.type == Gst.Message.EOS:
            pipeline.set_state(Gst.State.NULL)
        elif message.type == Gst.Message.ERROR:
            err, debug = message.parse_error()
            print(err, debug)
            pipeline.set_state(Gst.State.NULL)

    bus.connect('message', on_message)

    # Start pipeline
    pipeline.set_state(Gst.State.PLAYING)

    # Get sample from appsink
    sample = appsink.get_buffer()
    if sample:
        buf = sample.get_buffer()
        caps = sample.get_caps()
        arr = np.frombuffer(buf.get_data(), dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        cv2.imshow("Video", frame)
        cv2.waitKey(1)

    # Stop pipeline
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    main()
