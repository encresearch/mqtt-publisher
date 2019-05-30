"""File with most reading tests"""
import pytest

#TODO def test_connect_to_broker():
"""	from publisher.publisher import (
        HOST, PORT, KEEPALIVE, TOPIC, client_id, connect_to_broker
    )
    def on_connect(client, userdata, flags, rc):
        assert rc == 0 # assert the connection is successful
        client.disconnect() # Then disconnect
    def on_publish(client, userdata, result):
        pass # just pass for now
    client, connection = connect_to_broker(
        client_id=client_id,
        host=HOST,
        port=PORT,
        keepalive=KEEPALIVE,
        on_connect=on_connect,
        on_publish=on_publish
    )
    # Now, lets test a fake connection
"""

@pytest.fixture
def readings_df():
    from publisher.publisher import get_readings
    df = get_readings()
    return df

def test_expected_readings():
    """Outputs readings from all pins for calibration purposes."""
    from publisher.publisher import (
        Adafruit_ADS1x15,
        GAIN, data_rate,
        adc0,
        adc1,
        adc2,
        adc3
    )
    adcs = [(0, adc0), (1, adc1), (2, adc2), (3, adc3)]
    readings = []
    ansi_code_yellow_init = "\033[93m"
    ansi_code_yellow_end = "\033[00m"
    for adc in adcs:
        print('\n{}ADC: {}{}'.format(
            ansi_code_yellow_init,
            adc[0],
            ansi_code_yellow_end
        )), 
        for pin in range(4):
            reading = adc[1].read_adc(pin, gain=GAIN, data_rate=data_rate)*0.125
            assert reading is not None
            readings.append(reading)
            print('\t{}PIN: {}, READING: {} mV{}'.format(
                ansi_code_yellow_init,
                pin,
                reading,
                ansi_code_yellow_end
            ))
    if not all(reading is None for reading in readings):
        print("\n{}{}\n{}{}".format(
            ansi_code_yellow_init,
            "PLEASE MAKE SURE ALL READ VALUES ARE EXPECTED",
            ('#'*50),
            ansi_code_yellow_end
        ))

def test_readings_and_rate(readings_df):
    """Reads measurements for one minute."""
    import pandas as pd
    df = readings_df
    assert len(df) == 9600
    all_adcs_readings = df['adc'].value_counts()
    for readings in all_adcs_readings:
        assert readings == 2400
    # TODO test rates based on df

def test_send_readings(readings_df):
    import os 
    import pandas as pd
    from publisher.publisher import send_readings
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    send_readings(readings_df)
    # test a csv file is created
    assert os.path.exists('{path}/{file}'.format(
        path=dir_path,
        file='ten_hz.csv'
    ))
    # TODO: Test a CSV file is sent to the broker (with a fake broker container)
    pass
