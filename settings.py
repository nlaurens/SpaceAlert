class Settings:
    soundsDir = 'sounds/'

    sound = {}
    messg = {}

    #Alerts
    sound['AL'] = 'alert.mp3'
    messg['AL'] = 'Alert'

    # Note the %s is the number of the phase (i.e. 1 to 8)
    sound['ALP'] = 'time_t_plus_%s.mp3'
    messg['ALP'] = 'time t+%s'

    sound['ALTT'] = 'threat.mp3'
    messg['ALTT'] = 'incoming threat'
    sound['ALTST'] = 'serious_threat.mp3'
    messg['ALTST'] = 'incoming serious threat'
    sound['ALTIT'] = 'internal_threat.mp3'
    messg['ALTIT'] = 'internal threat'
    sound['ALTSIT'] = 'serious_internal_threat.mp3'
    messg['ALTSIT'] = 'serious internal threat'

    sound['ALZB'] = 'zone_Blue.mp3'
    messg['ALZB'] = 'zone blue'
    sound['ALZR'] = 'zone_Red.mp3'
    messg['ALZR'] = 'zone red'
    sound['ALZW'] = 'zone_White.mp3'
    messg['ALZW'] = 'zone white'

    sound['repeat'] = 'repeat.mp3'
    messg['repeat'] = 'I repeat:'

    # Phase Events
    sound['begin'] = 'begin_first_phase.mp3'
    messg['begin'] = 'Alert! Enemy activity detected. Please begin first phase.'

    sound['PE11M'] = 'first_phase_ends_in_1_minute.mp3'
    messg['PE11M'] = 'First phase will ends in 1 minute!'
    sound['PE120S'] = 'first_phase_ends_in_20_seconds.mp3'
    messg['PE120S'] = 'First phase will end in 20 seconds!'
    sound['PE1'] = 'first_phase_ends.mp3'
    messg['PE1'] = 'First phase will end!'

    sound['PE21M'] = 'second_phase_ends_in_1_minute.mp3'
    messg['PE21M'] = 'Second phase will ends in 1 minute!'
    sound['PE220S'] = 'second_phase_ends_in_20_seconds.mp3'
    messg['PE220S'] = 'Second phase will end in 20 seconds!'
    sound['PE2'] = 'second_phase_ends.mp3'
    messg['PE2'] = 'Second phase will end!'

    sound['begin_second_phase'] = 'second_phase_begins.mp3'
    messg['begin_second_phase'] = 'Please begin second phase!'

    #Unconfirmed report
    sound['UR'] = 'unconfirmed_report.mp3'
    messg['UR'] = 'Unconfirmed report!'

    #Incoming Data
    sound['ID'] = 'incoming_data.mp3'
    messg['ID'] = 'Incoming data!'

    #Data Transfer
    sound['DT'] = 'data_transfer.mp3'
    messg['DT'] = 'Data transfer!'

    # Communications System Down (Note! Always start the sound with CS%s-).
    # It's a dirty hack for making sure the communications don't run to long or
    # short.
    sound['CS'] = 'CS%s-communications_down.mp3'
    messg['CS'] = 'Communications down!'

    sound['noise'] = 'white_noise.mp3'

    sound['CSRestored'] = 'communications_restored.mp3'
