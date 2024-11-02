
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))



if __name__ == '__main__':
    from dashcam import app
    application = app(debug=True)
    application.run()
    # application.camera_calibration()

