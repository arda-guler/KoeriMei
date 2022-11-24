import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import keyboard
import time

import koeri
from globe import Earth_globe
from graphics import *
from camera import *
from turkiye import turkiye_cities

cameras = []

def current_time():
    return time.perf_counter()

def update_koeri():
    EQlist = koeri.generate_quakes()
    return EQlist

def window_resize(window, width, height):
    global cameras
    glViewport(0, 0, width, height)
    glLoadIdentity()
    main_cam = cameras[0]
    gluPerspective(70, width/height, 1, 100000)
    glTranslate(main_cam.pos.x, main_cam.pos.y, main_cam.pos.z)
    main_cam.orient = [[1,0,0],
                       [0,1,0],
                       [0,0,1]]

def mei():
    global cameras
    
    print("Fetching and parsing earthquake list from KOERI...")
    EQlist = koeri.generate_quakes()

    if len(EQlist):
        print("Earthquake list acquired.")
    else:
        print("Earthquake list empty! (Good or bad news?)")
        input("Press Enter to quit...")
        return

    print("Generating globe...")
    main_globe = Earth_globe()
    print("Globe generated.")

    print("Initializing graphics...")
    glfw.init()
    window_x = 1280
    window_y = 720
    mwin = glfw.create_window(window_x, window_y, "Koeri Mei", None, None)
    glfw.set_window_pos(mwin, 50, 50)
    glfw.make_context_current(mwin)
    glfw.set_window_size_callback(mwin, window_resize)

    gluPerspective(70, window_x/window_y, 1, 100000)
    glClearColor(0,0,0,0)
    glEnable(GL_POINT_SMOOTH)
    
    main_cam = camera("main_cam", vec3(0,0,0), [[1,0,0],[0,1,0],[0,0,1]], True)
    cameras.append(main_cam)
    main_cam.move(vec3(-4550, -3050, -5500))
    main_cam.rotate(vec3(0,0,130))
    main_cam.rotate(vec3(20, 0, 0))

    # keyboard controls
    cam_pitch_down = "W"
    cam_pitch_up = "S"
    cam_yaw_left = "A"
    cam_yaw_right = "D"
    cam_roll_ccw = "Q"
    cam_roll_cw = "E"

    cam_strafe_left = "J"
    cam_strafe_right = "L"
    cam_strafe_down = "O"
    cam_strafe_up = "U"
    cam_strafe_forward = "I" 
    cam_strafe_backward = "K"

    reduce_strafe_speed = "G"
    increase_strafe_speed = "T"

    update_koeri_btn = "V"

    cam_rotate_speed = 0.2
    cam_strafe_speed = 10

    speed_control_lock = False
    update_koeri_lock = False
    last_update_time = None

    print("Starting...")

    while not glfw.window_should_close(mwin):

        # get input and move the "camera" around
        rotation = vec3((keyboard.is_pressed(cam_pitch_down) - keyboard.is_pressed(cam_pitch_up)) * cam_rotate_speed,
                        (keyboard.is_pressed(cam_yaw_left) - keyboard.is_pressed(cam_yaw_right)) * cam_rotate_speed,
                        (keyboard.is_pressed(cam_roll_ccw) - keyboard.is_pressed(cam_roll_cw)) * cam_rotate_speed)
        main_cam.rotate(rotation)

        movement = vec3((keyboard.is_pressed(cam_strafe_left) - keyboard.is_pressed(cam_strafe_right)) * cam_strafe_speed,
                        (keyboard.is_pressed(cam_strafe_down) - keyboard.is_pressed(cam_strafe_up)) * cam_strafe_speed,
                        (keyboard.is_pressed(cam_strafe_forward) - keyboard.is_pressed(cam_strafe_backward)) * cam_strafe_speed)

        main_cam.move(movement)

        if not speed_control_lock and keyboard.is_pressed(increase_strafe_speed):
            cam_strafe_speed *= 5
            speed_control_lock = True
        elif not speed_control_lock and keyboard.is_pressed(reduce_strafe_speed):
            cam_strafe_speed *= 0.2
            speed_control_lock = True
        elif speed_control_lock and not (keyboard.is_pressed(reduce_strafe_speed) or keyboard.is_pressed(increase_strafe_speed)):
            speed_control_lock = False

        if keyboard.is_pressed(update_koeri_btn) and not update_koeri_lock and (last_update_time==None or (current_time() - last_update_time > 30)):
            print("Updating latest earthquake data...")
            EQlist = update_koeri()
            last_update_time = current_time()
            print("Earthquake data updated.")
            update_koeri_lock = True
        elif keyboard.is_pressed(update_koeri_btn) and not (current_time() - last_update_time > 30):
            print("WARNING: Data update cancelled. DO NOT SPAM KOERI SERVERS! (Wait", str(30-(current_time() - last_update_time)), "seconds.)")
        elif update_koeri_lock and not keyboard.is_pressed(update_koeri_btn):
            update_koeri_lock = False
        
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawOrigin()
        drawEarthGlobe(main_globe, [0,0,0], [0,0,0,0], [1,1,1], [0,0,1])
        drawQuakes(EQlist)
        drawSettlements(turkiye_cities, main_cam)
        glfw.swap_buffers(mwin)

    print("Ending program...")
    glfw.destroy_window(mwin)
    return

mei()
