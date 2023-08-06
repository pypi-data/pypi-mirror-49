# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Tbex(KaitaiStruct):
    """:field dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.payload.pid
    :field primary_id: ax25_frame.payload.ax25_info.header.primary_id
    :field secondary_id: ax25_frame.payload.ax25_info.header.secondary_id
    :field flags: ax25_frame.payload.ax25_info.header.flags
    :field packet_length: ax25_frame.payload.ax25_info.header.packet_length
    :field header_checksum: ax25_frame.payload.ax25_info.header.header_checksum
    :field operation_mode: ax25_frame.payload.ax25_info.payload.beacon_type.operation_mode
    :field rtc_unix_time: ax25_frame.payload.ax25_info.payload.beacon_type.rtc_unix_time
    :field numresets: ax25_frame.payload.ax25_info.payload.beacon_type.numresets
    :field avgnumactivetasks1: ax25_frame.payload.ax25_info.payload.beacon_type.avgnumactivetasks1
    :field avgnumactivetasks5: ax25_frame.payload.ax25_info.payload.beacon_type.avgnumactivetasks5
    :field avgnumactivetasks15: ax25_frame.payload.ax25_info.payload.beacon_type.avgnumactivetasks15
    :field totnumprocesses: ax25_frame.payload.ax25_info.payload.beacon_type.totnumprocesses
    :field usedmemminuscache: ax25_frame.payload.ax25_info.payload.beacon_type.usedmemminuscache
    :field freemempluscache: ax25_frame.payload.ax25_info.payload.beacon_type.freemempluscache
    :field sd_usage: ax25_frame.payload.ax25_info.payload.beacon_type.sd_usage
    :field datamnt_usage: ax25_frame.payload.ax25_info.payload.beacon_type.datamnt_usage
    :field stamp_gpio_states: ax25_frame.payload.ax25_info.payload.beacon_type.stamp_gpio_states
    :field ioe_states: ax25_frame.payload.ax25_info.payload.beacon_type.ioe_states
    :field lithium_op_count: ax25_frame.payload.ax25_info.payload.beacon_type.lithium_op_count
    :field lithium_msp430_temp: ax25_frame.payload.ax25_info.payload.beacon_type.lithium_msp430_temp
    :field lithium_rssi: ax25_frame.payload.ax25_info.payload.beacon_type.lithium_rssi
    :field lithium_rx: ax25_frame.payload.ax25_info.payload.beacon_type.lithium_rx
    :field lithium_tx: ax25_frame.payload.ax25_info.payload.beacon_type.lithium_tx
    :field fcpu_processor_temp: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_processor_temp
    :field lithium_pa_temp: ax25_frame.payload.ax25_info.payload.beacon_type.lithium_pa_temp
    :field li_3v3_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.li_3v3_voltage
    :field fcpu_3v3_current: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_3v3_current
    :field li_3v3_current: ax25_frame.payload.ax25_info.payload.beacon_type.li_3v3_current
    :field fcpu_3v3_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_3v3_voltage
    :field li_vbatt_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.li_vbatt_voltage
    :field li_vbatt_current: ax25_frame.payload.ax25_info.payload.beacon_type.li_vbatt_current
    :field sd_imon_1: ax25_frame.payload.ax25_info.payload.beacon_type.sd_imon_1
    :field sd_imon_2: ax25_frame.payload.ax25_info.payload.beacon_type.sd_imon_2
    :field sd_imon_3: ax25_frame.payload.ax25_info.payload.beacon_type.sd_imon_3
    :field sd_imon_4: ax25_frame.payload.ax25_info.payload.beacon_type.sd_imon_4
    :field battery_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.battery_voltage
    :field battery_current: ax25_frame.payload.ax25_info.payload.beacon_type.battery_current
    :field battery_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.battery_temperature
    :field battery_bus_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.battery_bus_voltage
    :field battery_bus_current: ax25_frame.payload.ax25_info.payload.beacon_type.battery_bus_current
    :field bus_voltage_5v: ax25_frame.payload.ax25_info.payload.beacon_type.bus_voltage_5v
    :field bus_current_5v: ax25_frame.payload.ax25_info.payload.beacon_type.bus_current_5v
    :field input_current_5v: ax25_frame.payload.ax25_info.payload.beacon_type.input_current_5v
    :field bus_voltage_3_3v: ax25_frame.payload.ax25_info.payload.beacon_type.bus_voltage_3_3v
    :field bus_current_3_3v: ax25_frame.payload.ax25_info.payload.beacon_type.bus_current_3_3v
    :field input_current_3_3v: ax25_frame.payload.ax25_info.payload.beacon_type.input_current_3_3v
    :field output_regulator_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.output_regulator_temperature
    :field eps_5v_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.eps_5v_voltage
    :field eps_5v_current: ax25_frame.payload.ax25_info.payload.beacon_type.eps_5v_current
    :field eps_3_3_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.eps_3_3_voltage
    :field eps_3_3v_current: ax25_frame.payload.ax25_info.payload.beacon_type.eps_3_3v_current
    :field channel_1_panel_voltage_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_1_panel_voltage_a
    :field channel_1_panel_voltage_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_1_panel_voltage_b
    :field channel_1_panel_current_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_1_panel_current_a
    :field channel_1_panel_current_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_1_panel_current_b
    :field channel_1_output_current: ax25_frame.payload.ax25_info.payload.beacon_type.channel_1_output_current
    :field channel_1_output_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.channel_1_output_voltage
    :field channel_1_board_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_1_board_temperature
    :field channel_1_module_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_1_module_temperature
    :field channel_2_panel_voltage_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_2_panel_voltage_a
    :field channel_2_panel_voltage_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_2_panel_voltage_b
    :field channel_2_panel_current_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_2_panel_current_a
    :field channel_2_panel_current_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_2_panel_current_b
    :field channel_2_output_current: ax25_frame.payload.ax25_info.payload.beacon_type.channel_2_output_current
    :field channel_2_output_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.channel_2_output_voltage
    :field channel_2_board_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_2_board_temperature
    :field channel_2_module_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_2_module_temperature
    :field channel_3_panel_voltage_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_3_panel_voltage_a
    :field channel_3_panel_voltage_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_3_panel_voltage_b
    :field channel_3_panel_current_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_3_panel_current_a
    :field channel_3_panel_current_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_3_panel_current_b
    :field channel_3_output_current: ax25_frame.payload.ax25_info.payload.beacon_type.channel_3_output_current
    :field channel_3_output_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.channel_3_output_voltage
    :field channel_3_board_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_3_board_temperature
    :field channel_3_module_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_3_module_temperature
    :field channel_4_panel_voltage_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_4_panel_voltage_a
    :field channel_4_panel_voltage_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_4_panel_voltage_b
    :field channel_4_panel_current_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_4_panel_current_a
    :field channel_4_panel_current_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_4_panel_current_b
    :field channel_4_output_current: ax25_frame.payload.ax25_info.payload.beacon_type.channel_4_output_current
    :field channel_4_output_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.channel_4_output_voltage
    :field channel_4_board_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_4_board_temperature
    :field channel_4_module_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_4_module_temperature
    :field channel_5_module_input_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.channel_5_module_input_voltage
    :field channel_5_panel_current_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_5_panel_current_a
    :field channel_5_panel_current_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_5_panel_current_b
    :field channel_5_output_current: ax25_frame.payload.ax25_info.payload.beacon_type.channel_5_output_current
    :field channel_5_board_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_5_board_temperature
    :field channel_5_module_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_5_module_temperature
    :field channel_6_module_input_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.channel_6_module_input_voltage
    :field channel_6_panel_current_a: ax25_frame.payload.ax25_info.payload.beacon_type.channel_6_panel_current_a
    :field channel_6_panel_current_b: ax25_frame.payload.ax25_info.payload.beacon_type.channel_6_panel_current_b
    :field channel_6_output_current: ax25_frame.payload.ax25_info.payload.beacon_type.channel_6_output_current
    :field channel_6_board_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_6_board_temperature
    :field channel_6_module_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.channel_6_module_temperature
    :field adcs_5v_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.adcs_5v_voltage
    :field adcs_5v_current: ax25_frame.payload.ax25_info.payload.beacon_type.adcs_5v_current
    :field adcs_3v3_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.adcs_3v3_voltage
    :field adcs_3v3_current: ax25_frame.payload.ax25_info.payload.beacon_type.adcs_3v3_current
    :field adcs_vbatt_curent: ax25_frame.payload.ax25_info.payload.beacon_type.adcs_vbatt_curent
    :field adcs_vbatt_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.adcs_vbatt_voltage
    :field adcs_temp_0: ax25_frame.payload.ax25_info.payload.beacon_type.adcs_temp_0
    :field adcs_temp_1: ax25_frame.payload.ax25_info.payload.beacon_type.adcs_temp_1
    :field eimu_current: ax25_frame.payload.ax25_info.payload.beacon_type.eimu_current
    :field adc_curr: ax25_frame.payload.ax25_info.payload.beacon_type.adc_curr
    :field sd_v: ax25_frame.payload.ax25_info.payload.beacon_type.sd_v
    :field fcpu_var_1: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_1
    :field fcpu_var_2: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_2
    :field fcpu_var_3: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_3
    :field fcpu_var_4: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_4
    :field fcpu_var_5: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_5
    :field fcpu_var_6: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_6
    :field tbex_payload_current: ax25_frame.payload.ax25_info.payload.beacon_type.tbex_payload_current
    :field tbex_payload_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.tbex_payload_voltage
    :field pim_3v3_current: ax25_frame.payload.ax25_info.payload.beacon_type.pim_3v3_current
    :field pim_3v3_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.pim_3v3_voltage
    :field pim_vbatt_monitor: ax25_frame.payload.ax25_info.payload.beacon_type.pim_vbatt_monitor
    :field pim_bus_3v3_voltag: ax25_frame.payload.ax25_info.payload.beacon_type.pim_bus_3v3_voltag
    :field rtc_unix_time_beacon_2: ax25_frame.payload.ax25_info.payload.beacon_type.rtc_unix_time_beacon_2
    :field numresets_beacon_2: ax25_frame.payload.ax25_info.payload.beacon_type.numresets_beacon_2
    :field stamp_gpio_states_abbreviated: ax25_frame.payload.ax25_info.payload.beacon_type.stamp_gpio_states_abbreviated
    :field fcpu_var_7: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_7
    :field fcpu_var_8: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_8
    :field fcpu_var_9: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_9
    :field fcpu_var_10: ax25_frame.payload.ax25_info.payload.beacon_type.fcpu_var_10
    :field command_received_from_fcpu: ax25_frame.payload.ax25_info.payload.beacon_type.command_received_from_fcpu
    :field nx_wing_magnetometer_x: ax25_frame.payload.ax25_info.payload.beacon_type.nx_wing_magnetometer_x
    :field nx_wing_magnetometer_y: ax25_frame.payload.ax25_info.payload.beacon_type.nx_wing_magnetometer_y
    :field nx_wing_magnetometer_z: ax25_frame.payload.ax25_info.payload.beacon_type.nx_wing_magnetometer_z
    :field px_wing_magnetometer_x: ax25_frame.payload.ax25_info.payload.beacon_type.px_wing_magnetometer_x
    :field px_wing_magnetometer_y: ax25_frame.payload.ax25_info.payload.beacon_type.px_wing_magnetometer_y
    :field px_wing_magnetometer_z: ax25_frame.payload.ax25_info.payload.beacon_type.px_wing_magnetometer_z
    :field py_body_magnetometer_x: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_magnetometer_x
    :field py_body_magnetometer_y: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_magnetometer_y
    :field py_body_magnetometer_z: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_magnetometer_z
    :field ny_body_magnetometer_x: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_magnetometer_x
    :field ny_body_magnetometer_y: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_magnetometer_y
    :field ny_body_magnetometer_z: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_magnetometer_z
    :field py_body_cell_voltage_1: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_cell_voltage_1
    :field py_body_cell_voltage_2: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_cell_voltage_2
    :field py_body_panel_circuitry_current: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_panel_circuitry_current
    :field py_body_internal_temp: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_internal_temp
    :field py_body_external_temp: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_external_temp
    :field ny_body_cell_voltage_1: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_cell_voltage_1
    :field ny_body_cell_voltage_2: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_cell_voltage_2
    :field ny_body_panel_circuitry_current: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_panel_circuitry_current
    :field ny_body_internal_temp: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_internal_temp
    :field ny_body_external_temp: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_external_temp
    :field nx_body_cell_voltage_1: ax25_frame.payload.ax25_info.payload.beacon_type.nx_body_cell_voltage_1
    :field nx_body_cell_voltage_2: ax25_frame.payload.ax25_info.payload.beacon_type.nx_body_cell_voltage_2
    :field nx_body_panel_circuitry_current: ax25_frame.payload.ax25_info.payload.beacon_type.nx_body_panel_circuitry_current
    :field nx_body_internal_temp: ax25_frame.payload.ax25_info.payload.beacon_type.nx_body_internal_temp
    :field nx_body_external_temp: ax25_frame.payload.ax25_info.payload.beacon_type.nx_body_external_temp
    :field px_body_cell_voltage_1: ax25_frame.payload.ax25_info.payload.beacon_type.px_body_cell_voltage_1
    :field px_body_cell_voltage_2: ax25_frame.payload.ax25_info.payload.beacon_type.px_body_cell_voltage_2
    :field px_body_panel_circuitry_current: ax25_frame.payload.ax25_info.payload.beacon_type.px_body_panel_circuitry_current
    :field px_body_internal_temp: ax25_frame.payload.ax25_info.payload.beacon_type.px_body_internal_temp
    :field px_body_external_temp: ax25_frame.payload.ax25_info.payload.beacon_type.px_body_external_temp
    :field nx_deployable_temp_1: ax25_frame.payload.ax25_info.payload.beacon_type.nx_deployable_temp_1
    :field nx_deployable_temp_2: ax25_frame.payload.ax25_info.payload.beacon_type.nx_deployable_temp_2
    :field nx_deployable_panel_circuitry_current: ax25_frame.payload.ax25_info.payload.beacon_type.nx_deployable_panel_circuitry_current
    :field px_deployable_temp_1: ax25_frame.payload.ax25_info.payload.beacon_type.px_deployable_temp_1
    :field px_deployable_temp_2: ax25_frame.payload.ax25_info.payload.beacon_type.px_deployable_temp_2
    :field px_deployable_panel_circuitry_current: ax25_frame.payload.ax25_info.payload.beacon_type.px_deployable_panel_circuitry_current
    :field py_deployable_temp_1: ax25_frame.payload.ax25_info.payload.beacon_type.py_deployable_temp_1
    :field py_deployable_temp_2: ax25_frame.payload.ax25_info.payload.beacon_type.py_deployable_temp_2
    :field py_deployable_panel_circuitry_current: ax25_frame.payload.ax25_info.payload.beacon_type.py_deployable_panel_circuitry_current
    :field ny_deployable_temp_1: ax25_frame.payload.ax25_info.payload.beacon_type.ny_deployable_temp_1
    :field ny_deployable_temp_2: ax25_frame.payload.ax25_info.payload.beacon_type.ny_deployable_temp_2
    :field ny_deployable_panel_circuitry_current: ax25_frame.payload.ax25_info.payload.beacon_type.ny_deployable_panel_circuitry_current
    :field nx_wing_photodiode_a: ax25_frame.payload.ax25_info.payload.beacon_type.nx_wing_photodiode_a
    :field nx_wing_photodiode_b: ax25_frame.payload.ax25_info.payload.beacon_type.nx_wing_photodiode_b
    :field px_wing_photodiode_a: ax25_frame.payload.ax25_info.payload.beacon_type.px_wing_photodiode_a
    :field px_wing_photodiode_b: ax25_frame.payload.ax25_info.payload.beacon_type.px_wing_photodiode_b
    :field py_body_photodiode_a: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_photodiode_a
    :field py_body_photodiode_b: ax25_frame.payload.ax25_info.payload.beacon_type.py_body_photodiode_b
    :field ny_body_photodiode_a: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_photodiode_a
    :field ny_body_photodiode_b: ax25_frame.payload.ax25_info.payload.beacon_type.ny_body_photodiode_b
    :field py_wing_photodiode_a: ax25_frame.payload.ax25_info.payload.beacon_type.py_wing_photodiode_a
    :field py_wing_photodiode_b: ax25_frame.payload.ax25_info.payload.beacon_type.py_wing_photodiode_b
    :field ny_wing_photodiode_a: ax25_frame.payload.ax25_info.payload.beacon_type.ny_wing_photodiode_a
    :field ny_wing_photodiode_b: ax25_frame.payload.ax25_info.payload.beacon_type.ny_wing_photodiode_b
    :field nx_body_photodiode_a: ax25_frame.payload.ax25_info.payload.beacon_type.nx_body_photodiode_a
    :field nx_body_photodiode_b: ax25_frame.payload.ax25_info.payload.beacon_type.nx_body_photodiode_b
    :field px_body_photodiode_a: ax25_frame.payload.ax25_info.payload.beacon_type.px_body_photodiode_a
    :field px_body_photodiode_b: ax25_frame.payload.ax25_info.payload.beacon_type.px_body_photodiode_b
    :field gyro_4_x: ax25_frame.payload.ax25_info.payload.beacon_type.gyro_4_x
    :field gyro_4_y: ax25_frame.payload.ax25_info.payload.beacon_type.gyro_4_y
    :field gyro_4_z: ax25_frame.payload.ax25_info.payload.beacon_type.gyro_4_z
    :field eimu_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.eimu_temperature
    :field wheel_x_speed: ax25_frame.payload.ax25_info.payload.beacon_type.wheel_x_speed
    :field wheel_y_speed: ax25_frame.payload.ax25_info.payload.beacon_type.wheel_y_speed
    :field wheel_z_speed: ax25_frame.payload.ax25_info.payload.beacon_type.wheel_z_speed
    :field tcb_temp_0: ax25_frame.payload.ax25_info.payload.beacon_type.tcb_temp_0
    :field tcb_3v3_current: ax25_frame.payload.ax25_info.payload.beacon_type.tcb_3v3_current
    :field tcb_vbatt_current: ax25_frame.payload.ax25_info.payload.beacon_type.tcb_vbatt_current
    :field input_current: ax25_frame.payload.ax25_info.payload.beacon_type.input_current
    :field input_voltage: ax25_frame.payload.ax25_info.payload.beacon_type.input_voltage
    :field voltage_5_5: ax25_frame.payload.ax25_info.payload.beacon_type.voltage_5_5
    :field voltage_3_0: ax25_frame.payload.ax25_info.payload.beacon_type.voltage_3_0
    :field voltage_3_3: ax25_frame.payload.ax25_info.payload.beacon_type.voltage_3_3
    :field rf_board_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.rf_board_temperature
    :field control_board_temperature: ax25_frame.payload.ax25_info.payload.beacon_type.control_board_temperature
    :field vhf_channel_forward_power: ax25_frame.payload.ax25_info.payload.beacon_type.vhf_channel_forward_power
    :field uhf_channel_forward_power: ax25_frame.payload.ax25_info.payload.beacon_type.uhf_channel_forward_power
    :field l_band_channel_forward_power: ax25_frame.payload.ax25_info.payload.beacon_type.l_band_channel_forward_power
    :field vhf_channel_reverse_power: ax25_frame.payload.ax25_info.payload.beacon_type.vhf_channel_reverse_power
    :field uhf_channel_reverse_power: ax25_frame.payload.ax25_info.payload.beacon_type.uhf_channel_reverse_power
    :field l_band_channel_reverse_power: ax25_frame.payload.ax25_info.payload.beacon_type.l_band_channel_reverse_power
    :field pll_config_mask: ax25_frame.payload.ax25_info.payload.beacon_type.pll_config_mask
    :field ppu_reset_count: ax25_frame.payload.ax25_info.payload.beacon_type.ppu_reset_count
    :field status_mask: ax25_frame.payload.ax25_info.payload.beacon_type.status_mask
    :field error_mask: ax25_frame.payload.ax25_info.payload.beacon_type.error_mask
    :field crc: ax25_frame.payload.crc
    
    .. seealso::
       Source - https://docs.google.com/spreadsheets/d/1mGekVQyf4Ozlf6UqojZk0ji02DwLLDFp3S1XTffvqGk/edit#gid=1694629037
       https://drive.google.com/file/d/1XduQg8NTiXD0MORRmrdjMPdAokTbSP_1/view
       https://drive.google.com/file/d/1mv0lSleUe6LL0O4OmI-LSaQlulIeozMu/view
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = self._root.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = self._root.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = self._root.IFrame(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = self._root.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = self._root.SsidMask(self._io, self, self._root)
            if (self.src_ssid_raw.ssid_mask & 1) == 0:
                self.repeater = self._root.Repeater(self._io, self, self._root)

            self.ctl = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            _on = self._parent.ax25_header.src_callsign_raw.callsign_ror.callsign
            if _on == u"KF6RFX":
                self._raw_ax25_info = self._io.read_bytes_full()
                io = KaitaiStream(BytesIO(self._raw_ax25_info))
                self.ax25_info = self._root.TbexPacketT(io, self, self._root)
            else:
                self.ax25_info = self._io.read_bytes_full()


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class TbexHeaderT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sync = self._io.ensure_fixed_contents(b"\xAB\xCD")
            self.primary_id = self._io.read_u2le()
            self.secondary_id = self._io.read_u2le()
            self.flags = self._io.read_u1()
            self.packet_length = self._io.read_u2le()
            self.header_checksum = self._io.read_u2le()


    class Beacon1T(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.operation_mode = self._io.read_u2le()
            self.rtc_unix_time = self._io.read_u4le()
            self.numresets = self._io.read_u2le()
            self.avgnumactivetasks1 = self._io.read_u2le()
            self.avgnumactivetasks5 = self._io.read_u2le()
            self.avgnumactivetasks15 = self._io.read_u2le()
            self.totnumprocesses = self._io.read_u2le()
            self.usedmemminuscache = self._io.read_u2le()
            self.freemempluscache = self._io.read_u2le()
            self.sd_usage = self._io.read_u2le()
            self.datamnt_usage = self._io.read_u2le()
            self.stamp_gpio_states = self._io.read_u2le()
            self.ioe_states = self._io.read_u1()
            self.lithium_op_count = self._io.read_u2le()
            self.lithium_msp430_temp = self._io.read_s2le()
            self.lithium_rssi = self._io.read_u1()
            self.lithium_rx = self._io.read_u4le()
            self.lithium_tx = self._io.read_u4le()
            self.fcpu_processor_temp = self._io.read_s2le()
            self.lithium_pa_temp = self._io.read_s2le()
            self.li_3v3_voltage = self._io.read_u2le()
            self.fcpu_3v3_current = self._io.read_u2le()
            self.li_3v3_current = self._io.read_u2le()
            self.fcpu_3v3_voltage = self._io.read_u2le()
            self.li_vbatt_voltage = self._io.read_u2le()
            self.li_vbatt_current = self._io.read_u2le()
            self.sd_imon_1 = self._io.read_u2le()
            self.sd_imon_2 = self._io.read_u2le()
            self.sd_imon_3 = self._io.read_u2le()
            self.sd_imon_4 = self._io.read_u2le()
            self.battery_voltage = self._io.read_u2le()
            self.battery_current = self._io.read_s2le()
            self.battery_temperature = self._io.read_u2le()
            self.battery_bus_voltage = self._io.read_u2le()
            self.battery_bus_current = self._io.read_u2le()
            self.bus_voltage_5v = self._io.read_u2le()
            self.bus_current_5v = self._io.read_u2le()
            self.input_current_5v = self._io.read_u2le()
            self.bus_voltage_3_3v = self._io.read_u2le()
            self.bus_current_3_3v = self._io.read_u2le()
            self.input_current_3_3v = self._io.read_u2le()
            self.output_regulator_temperature = self._io.read_u2le()
            self.eps_5v_voltage = self._io.read_u2le()
            self.eps_5v_current = self._io.read_u2le()
            self.eps_3_3_voltage = self._io.read_s2le()
            self.eps_3_3v_current = self._io.read_s2le()
            self.channel_1_panel_voltage_a = self._io.read_u2le()
            self.channel_1_panel_voltage_b = self._io.read_u2le()
            self.channel_1_panel_current_a = self._io.read_u2le()
            self.channel_1_panel_current_b = self._io.read_u2le()
            self.channel_1_output_current = self._io.read_u2le()
            self.channel_1_output_voltage = self._io.read_u2le()
            self.channel_1_board_temperature = self._io.read_s2le()
            self.channel_1_module_temperature = self._io.read_s2le()
            self.channel_2_panel_voltage_a = self._io.read_u2le()
            self.channel_2_panel_voltage_b = self._io.read_u2le()
            self.channel_2_panel_current_a = self._io.read_u2le()
            self.channel_2_panel_current_b = self._io.read_u2le()
            self.channel_2_output_current = self._io.read_u2le()
            self.channel_2_output_voltage = self._io.read_u2le()
            self.channel_2_board_temperature = self._io.read_s2le()
            self.channel_2_module_temperature = self._io.read_s2le()
            self.channel_3_panel_voltage_a = self._io.read_u2le()
            self.channel_3_panel_voltage_b = self._io.read_u2le()
            self.channel_3_panel_current_a = self._io.read_u2le()
            self.channel_3_panel_current_b = self._io.read_u2le()
            self.channel_3_output_current = self._io.read_u2le()
            self.channel_3_output_voltage = self._io.read_u2le()
            self.channel_3_board_temperature = self._io.read_s2le()
            self.channel_3_module_temperature = self._io.read_s2le()
            self.channel_4_panel_voltage_a = self._io.read_u2le()
            self.channel_4_panel_voltage_b = self._io.read_u2le()
            self.channel_4_panel_current_a = self._io.read_u2le()
            self.channel_4_panel_current_b = self._io.read_u2le()
            self.channel_4_output_current = self._io.read_u2le()
            self.channel_4_output_voltage = self._io.read_u2le()
            self.channel_4_board_temperature = self._io.read_s2le()
            self.channel_4_module_temperature = self._io.read_s2le()
            self.channel_5_module_input_voltage = self._io.read_u2le()
            self.channel_5_panel_current_a = self._io.read_u2le()
            self.channel_5_panel_current_b = self._io.read_u2le()
            self.channel_5_output_current = self._io.read_u2le()
            self.channel_5_board_temperature = self._io.read_s2le()
            self.channel_5_module_temperature = self._io.read_s2le()
            self.channel_6_module_input_voltage = self._io.read_u2le()
            self.channel_6_panel_current_a = self._io.read_u2le()
            self.channel_6_panel_current_b = self._io.read_u2le()
            self.channel_6_output_current = self._io.read_u2le()
            self.channel_6_board_temperature = self._io.read_s2le()
            self.channel_6_module_temperature = self._io.read_s2le()
            self.adcs_5v_voltage = self._io.read_u2le()
            self.adcs_5v_current = self._io.read_u2le()
            self.adcs_3v3_voltage = self._io.read_u2le()
            self.adcs_3v3_current = self._io.read_u2le()
            self.adcs_vbatt_curent = self._io.read_u2le()
            self.adcs_vbatt_voltage = self._io.read_u2le()
            self.adcs_temp_0 = self._io.read_s2le()
            self.adcs_temp_1 = self._io.read_s2le()
            self.eimu_current = self._io.read_u2le()
            self.adc_curr = self._io.read_u2le()
            self.sd_v = self._io.read_u2le()
            self.fcpu_var_1 = self._io.read_u1()
            self.fcpu_var_2 = self._io.read_u1()
            self.fcpu_var_3 = self._io.read_u1()
            self.fcpu_var_4 = self._io.read_u1()
            self.fcpu_var_5 = self._io.read_u1()
            self.fcpu_var_6 = self._io.read_u1()
            self.tbex_payload_current = self._io.read_u2le()
            self.tbex_payload_voltage = self._io.read_u2le()
            self.pim_3v3_current = self._io.read_u2le()
            self.pim_3v3_voltage = self._io.read_u2le()
            self.pim_vbatt_monitor = self._io.read_u2le()
            self.pim_bus_3v3_voltag = self._io.read_u2le()


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.ax25_info = self._io.read_bytes_full()


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return self._m_ssid if hasattr(self, '_m_ssid') else None


    class Repeaters(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.rpt_ssid_raw = self._root.SsidMask(self._io, self, self._root)


    class Repeater(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_instance = []
            i = 0
            while True:
                _ = self._root.Repeaters(self._io, self, self._root)
                self.rpt_instance.append(_)
                if (_.rpt_ssid_raw.ssid_mask & 1) == 1:
                    break
                i += 1


    class Beacon2T(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rtc_unix_time_beacon_2 = self._io.read_u4le()
            self.numresets_beacon_2 = self._io.read_u2le()
            self.stamp_gpio_states_abbreviated = self._io.read_u1()
            self.fcpu_var_7 = self._io.read_u1()
            self.fcpu_var_8 = self._io.read_u1()
            self.fcpu_var_9 = self._io.read_u1()
            self.fcpu_var_10 = self._io.read_u1()
            self.command_received_from_fcpu = self._io.read_u2le()
            self.nx_wing_magnetometer_x = self._io.read_s2le()
            self.nx_wing_magnetometer_y = self._io.read_s2le()
            self.nx_wing_magnetometer_z = self._io.read_s2le()
            self.px_wing_magnetometer_x = self._io.read_s2le()
            self.px_wing_magnetometer_y = self._io.read_s2le()
            self.px_wing_magnetometer_z = self._io.read_s2le()
            self.py_body_magnetometer_x = self._io.read_s2le()
            self.py_body_magnetometer_y = self._io.read_s2le()
            self.py_body_magnetometer_z = self._io.read_s2le()
            self.ny_body_magnetometer_x = self._io.read_s2le()
            self.ny_body_magnetometer_y = self._io.read_s2le()
            self.ny_body_magnetometer_z = self._io.read_s2le()
            self.py_body_cell_voltage_1 = self._io.read_u2le()
            self.py_body_cell_voltage_2 = self._io.read_u2le()
            self.py_body_panel_circuitry_current = self._io.read_u2le()
            self.py_body_internal_temp = self._io.read_s2le()
            self.py_body_external_temp = self._io.read_s2le()
            self.ny_body_cell_voltage_1 = self._io.read_u2le()
            self.ny_body_cell_voltage_2 = self._io.read_u2le()
            self.ny_body_panel_circuitry_current = self._io.read_u2le()
            self.ny_body_internal_temp = self._io.read_s2le()
            self.ny_body_external_temp = self._io.read_s2le()
            self.nx_body_cell_voltage_1 = self._io.read_u2le()
            self.nx_body_cell_voltage_2 = self._io.read_u2le()
            self.nx_body_panel_circuitry_current = self._io.read_u2le()
            self.nx_body_internal_temp = self._io.read_s2le()
            self.nx_body_external_temp = self._io.read_s2le()
            self.px_body_cell_voltage_1 = self._io.read_u2le()
            self.px_body_cell_voltage_2 = self._io.read_u2le()
            self.px_body_panel_circuitry_current = self._io.read_u2le()
            self.px_body_internal_temp = self._io.read_s2le()
            self.px_body_external_temp = self._io.read_s2le()
            self.nx_deployable_temp_1 = self._io.read_s2le()
            self.nx_deployable_temp_2 = self._io.read_s2le()
            self.nx_deployable_panel_circuitry_current = self._io.read_u2le()
            self.px_deployable_temp_1 = self._io.read_s2le()
            self.px_deployable_temp_2 = self._io.read_s2le()
            self.px_deployable_panel_circuitry_current = self._io.read_u2le()
            self.py_deployable_temp_1 = self._io.read_s2le()
            self.py_deployable_temp_2 = self._io.read_s2le()
            self.py_deployable_panel_circuitry_current = self._io.read_u2le()
            self.ny_deployable_temp_1 = self._io.read_s2le()
            self.ny_deployable_temp_2 = self._io.read_s2le()
            self.ny_deployable_panel_circuitry_current = self._io.read_u2le()
            self.nx_wing_photodiode_a = self._io.read_u2le()
            self.nx_wing_photodiode_b = self._io.read_u2le()
            self.px_wing_photodiode_a = self._io.read_u2le()
            self.px_wing_photodiode_b = self._io.read_u2le()
            self.py_body_photodiode_a = self._io.read_u2le()
            self.py_body_photodiode_b = self._io.read_u2le()
            self.ny_body_photodiode_a = self._io.read_u2le()
            self.ny_body_photodiode_b = self._io.read_u2le()
            self.py_wing_photodiode_a = self._io.read_u2le()
            self.py_wing_photodiode_b = self._io.read_u2le()
            self.ny_wing_photodiode_a = self._io.read_u2le()
            self.ny_wing_photodiode_b = self._io.read_u2le()
            self.nx_body_photodiode_a = self._io.read_u2le()
            self.nx_body_photodiode_b = self._io.read_u2le()
            self.px_body_photodiode_a = self._io.read_u2le()
            self.px_body_photodiode_b = self._io.read_u2le()
            self.gyro_4_x = self._io.read_s2le()
            self.gyro_4_y = self._io.read_s2le()
            self.gyro_4_z = self._io.read_s2le()
            self.eimu_temperature = self._io.read_s2le()
            self.wheel_x_speed = self._io.read_s2le()
            self.wheel_y_speed = self._io.read_s2le()
            self.wheel_z_speed = self._io.read_s2le()
            self.tcb_temp_0 = self._io.read_s2le()
            self.tcb_3v3_current = self._io.read_u2le()
            self.tcb_vbatt_current = self._io.read_u2le()
            self.input_current = self._io.read_u2le()
            self.input_voltage = self._io.read_u2le()
            self.voltage_5_5 = self._io.read_u2le()
            self.voltage_3_0 = self._io.read_u2le()
            self.voltage_3_3 = self._io.read_u2le()
            self.rf_board_temperature = self._io.read_u2le()
            self.control_board_temperature = self._io.read_u2le()
            self.vhf_channel_forward_power = self._io.read_u2le()
            self.uhf_channel_forward_power = self._io.read_u2le()
            self.l_band_channel_forward_power = self._io.read_u2le()
            self.vhf_channel_reverse_power = self._io.read_u2le()
            self.uhf_channel_reverse_power = self._io.read_u2le()
            self.l_band_channel_reverse_power = self._io.read_u2le()
            self.pll_config_mask = self._io.read_u1()
            self.ppu_reset_count = self._io.read_u1()
            self.status_mask = self._io.read_u1()
            self.error_mask = self._io.read_u2le()
            self.crc = self._io.read_u2le()


    class TbexBeaconT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self._root.framelength
            if _on == 219:
                self.beacon_type = self._root.Beacon2T(self._io, self, self._root)
            elif _on == 255:
                self.beacon_type = self._root.Beacon1T(self._io, self, self._root)


    class TbexPacketT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_header = self._io.read_bytes(11)
            io = KaitaiStream(BytesIO(self._raw_header))
            self.header = self._root.TbexHeaderT(io, self, self._root)
            _on = self.header.secondary_id
            if _on == 82:
                self.payload = self._root.TbexBeaconT(self._io, self, self._root)
            elif _on == 83:
                self.payload = self._root.TbexBeaconT(self._io, self, self._root)
            self.crc = self._io.read_u4le()


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            io = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = self._root.Callsign(io, self, self._root)


    @property
    def framelength(self):
        if hasattr(self, '_m_framelength'):
            return self._m_framelength if hasattr(self, '_m_framelength') else None

        self._m_framelength = self._io.size()
        return self._m_framelength if hasattr(self, '_m_framelength') else None


