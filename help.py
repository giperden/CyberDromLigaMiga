from pioneer_sdk import Pioneer
from pioneer_sdk import Camera

pioner = Pioneer(ip='127.0.0.1', mavlink_port=8001)
camera = Camera(ip='127.0.0.1', port=18001, timeout=3)
# Выводим список всех публичных методов для Pioneer
print([method for method in dir(pioner) if not method.startswith('_')])
#output :['AUTOPILOT_STATE', 'MAV_RESULT', 'ap_set_password', 'ap_set_ssid', 'arm', 'close_connection', 'connected', 'connection', 'disarm', 'get_autopilot_state', 'get_autopilot_version', 'get_battery_status', 'get_dist_sensor_data', 'get_local_position_lps', 'get_optical_data', 'get_preflight_state', 'go_to_local_point', 'go_to_local_point_body_fixed', 'land', 'led_control', 'log', 'lua_script_control', 'lua_script_upload', 'mavlink_socket', 'msg_archive', 'name', 'point_reached', 'raspberry_led_custom', 'raspberry_poweroff', 'raspberry_reboot', 'raspberry_start_capture', 'raspberry_stop_capture', 'reboot_board', 'receive_wifi_config_ap', 'send_ap_password', 'send_ap_ssid', 'send_rc_channels', 'send_sta_connect', 'send_sta_disconnect', 'set_log_connection', 'set_logger', 'set_manual_speed', 'set_manual_speed_body_fixed', 'sta_connect', 'sta_disconnect', 'takeoff', 'try_get_ap_status', 'try_get_sta_status', 'wait_msg']

# Выводим список всех публичных методов для Camera
print([method for method in dir(camera) if not method.startswith('_')])
#output: ['VIDEO_BUFFER_SIZE', 'connect', 'connected', 'disconnect', 'get_cv_frame', 'get_frame', 'ip', 'log_connection', 'new_tcp', 'new_udp', 'port', 'raw_video_frame', 'tcp', 'timeout', 'udp']