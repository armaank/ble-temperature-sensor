
#include "boards.h"
#include "nrf_log.h"
#include "nrf_delay.h"
#include "nrf_drv_adc.h"

#include "user_adc.h"

#define THERMISTOR_ADC_CH		ADC_CONFIG_PSEL_AnalogInput2

#define ADC_BUFFER_SIZE 		1                                	/**< Size of buffer for ADC samples.  */

typedef struct tagTHERMISTOR_INFO {
	int16_t		temperature;
	uint32_t	resistance;
} THERMISTOR_INFO;

const THERMISTOR_INFO c_thermistor_info_table[] = 
	{	{-40, 277200},	
		{-39, 263600},	{-38, 250100},	{-37, 236800}, 	{-36, 224000},	{-35, 211500},	{-34, 199600},	{-33, 188100},	{-32, 177300},	{-31, 167000},	{-30, 157200},
		{-29, 148100},	{-28, 139400},	{-27, 131300}, 	{-26, 123700},	{-25, 116600},	{-24, 110000},	{-23, 103700},	{-22, 97900},	{-21, 92500},	{-20, 87430},
		{-19, 82790},	{-18, 78440},	{-17, 74360}, 	{-16, 70530},	{-15, 66920},	{-14, 63540},	{-13, 60340},	{-12, 57330},	{-11, 54500},	{-10, 51820},
		{-9, 49280},	{-8, 46890},	{-7, 44620},	{-6, 42480},	{-5, 40450},	{-4, 38530},	{-3, 36700},	{-2, 34970},	{-1, 33330},	{0, 31770},
			
		{1, 30250},		{2, 28820},		{3, 27450}, 	{4, 26160},		{5, 24940},		{6, 23770},		{7, 22670},		{8, 21620},		{9, 20630},		{10, 19680},
		{11, 18780},	{12, 17930},	{13, 17120}, 	{14, 16350},	{15, 15620},	{16, 14930},	{17, 14260},	{18, 13630},	{19, 13040},	{20, 12470},
		{21, 11920},	{22, 11410},	{23, 10910}, 	{24, 10450},	{25, 10000},	{26, 9575},		{27, 9170},		{28, 8784},		{29, 8416},		{30, 8064},
		{31, 7730},		{32, 7410},		{33, 7106}, 	{34, 6815},		{35, 6538},		{36, 6273},		{37, 6020},		{38, 5778},		{39, 5548},		{40, 5327},
		{41, 5117},		{42, 4915},		{43, 4723}, 	{44, 4539},		{45, 4363},		{46, 4195},		{47, 4034},		{48, 3880},		{49, 3733},		{50, 3592},
		{51, 3457},		{52, 3328},		{53, 3204}, 	{54, 3086},		{55, 2972},		{56, 2863},		{57, 2759},		{58, 2659},		{59, 2564},		{60, 2472},
		{61, 2384},		{62, 2299},		{63, 2218}, 	{64, 2141},		{65, 2066},		{66, 1994},		{67, 1926},		{68, 1860},		{69, 1796},		{70, 1735},
		{71, 1677},		{72, 1621},		{73, 1567}, 	{74, 1515},		{75, 1465},		{76, 1417},		{77, 1371},		{78, 1326},		{79, 1284},		{80, 1243},
		{81, 1203},		{82, 1165},		{83, 1128}, 	{84, 1093},		{85, 1059},		{86, 1027},		{87, 996},		{88, 965},		{89, 936},		{90, 908},
		{91, 881},		{92, 855},		{93, 830}, 		{94, 805},		{95, 782},		{96, 759},		{97, 737},		{98, 715},		{99, 695},		{100, 674},
											
		{101, 656},		{102, 638},		{103, 620}, 	{104, 603},		{105, 586},		{106, 569},		{107, 554},		{108, 538},		{109, 523},		{110, 508},
		{111, 494},		{112, 480},		{113, 467}, 	{114, 454},		{115, 441},		{116, 429},		{117, 417},		{118, 406},		{119, 394},		{120, 384},
		{121, 373},		{122, 363},		{123, 353}, 	{124, 343},		{125, 334},		{126, 325},		{127, 317},		{128, 308},		{129, 300},		{130, 292},
		{131, 285},		{132, 277},		{133, 270}, 	{134, 263},		{135, 257},		{136, 250},		{137, 244},		{138, 238},		{139, 232},		{140, 226},
		{141, 220},		{142, 215},		{143, 210}, 	{144, 204},		{145, 199},		{146, 195},		{147, 190},		{148, 186},		{149, 181},		{150, 177},
		{151, 173},		{152, 169},		{153, 165}, 	{154, 161},		{155, 158},		{156, 154},		{157, 151},		{158, 147},		{159, 144},		{160, 141},
		{161, 138},		{162, 135},		{163, 132}, 	{164, 129},		{165, 127},		{166, 124},		{167, 121},		{168, 119},		{169, 116},		{170, 114},
		{171, 112},		{172, 109},		{173, 107}, 	{174, 105},		{175, 103},		{176, 101},		{177, 99},		{178, 97},		{179, 95},		{180, 93},
		{181, 91},		{182, 89},		{183, 87}, 		{184, 86},		{185, 84},		{186, 82},		{187, 81},		{188, 79},		{189, 77},		{190, 76},
		{191, 74},		{192, 73},		{193, 71}, 		{194, 70},		{195, 69},		{196, 67},		{197, 66},		{198, 65},		{199, 63},		{200, 62}
	};

static nrf_adc_value_t       	m_adc_buffer[ADC_BUFFER_SIZE];		/**< ADC buffer. */

static nrf_drv_adc_channel_t 	m_channel_config = 	{
														{
															{          
															.resolution = NRF_ADC_CONFIG_RES_10BIT,                
															.input      = NRF_ADC_CONFIG_SCALING_INPUT_ONE_THIRD, 
															.reference  = NRF_ADC_CONFIG_REF_SUPPLY_ONE_THIRD,	//NRF_ADC_CONFIG_REF_VBG,                  
															.ain        = THERMISTOR_ADC_CH // analog input
															}
														}, 
														NULL
													};

int16_t m_average_adc_val;

static void adc_event_handler(nrf_drv_adc_evt_t const * p_event)
{	
    if (p_event->type == NRF_DRV_ADC_EVT_DONE) // last
    {
        int32_t i; 
		int32_t sum 		= 0; // initialize sum to zero
		int32_t buf_size 	= p_event->data.done.size; // used for averaging 
		
		if (buf_size == 0) return;
		
        for (i = 0; i < buf_size; i++) {
//            NRF_LOG_INFO("Current sample value: %d\r\n", p_event->data.done.p_buffer[i]);		
			
			sum += (int32_t)p_event->data.done.p_buffer[i]; // accumulation
        }
		m_average_adc_val = (int16_t)(sum / buf_size);
    }
}

static int16_t UserADC_GetValue(uint32_t adc_ch)
{
    nrf_drv_adc_config_t 	adc_config	= NRF_DRV_ADC_DEFAULT_CONFIG;
	
	APP_ERROR_CHECK(nrf_drv_adc_init(&adc_config, adc_event_handler));	
	
	m_channel_config.config.config.ain = adc_ch;
    nrf_drv_adc_channel_enable(&m_channel_config);
	
	nrf_drv_adc_buffer_convert(m_adc_buffer, ADC_BUFFER_SIZE);
	nrf_drv_adc_sample();
	nrf_delay_ms(10);
	
    nrf_drv_adc_channel_disable(&m_channel_config);
	nrf_drv_adc_uninit();
	
	NRF_LOG_INFO("adc_val = %d\r\n", m_average_adc_val);	
	return m_average_adc_val;
}

int16_t Thermistor_GetValue(void)	// temperature between -40 ~ 200
{
	int16_t		temperature_val;
	int16_t 	adc_val 			= UserADC_GetValue(THERMISTOR_ADC_CH); // analog input 2
	
	if (adc_val < 0) 	adc_val = 0; // boundry/overflow error
	if (adc_val > 1023) adc_val = 1023; // boundry/overflow error
	
	uint32_t 	temp_resistance 	= adc_val * 10000 / (1024 - adc_val); // formula
	int 		table_count 		= sizeof(c_thermistor_info_table) / sizeof(THERMISTOR_INFO);
	int			i;
	
	NRF_LOG_INFO("temp_resistance = %d\n", temp_resistance);
	// boundry checking & error handling (if temp is lt -40 or gt 200 C) 
	if (temp_resistance < c_thermistor_info_table[table_count - 1].resistance) return c_thermistor_info_table[table_count - 1].temperature;
	else if (temp_resistance > c_thermistor_info_table[0].resistance) return c_thermistor_info_table[0].temperature;
	// determines i from table values	
	for (i = 0; i < table_count - 1; i++) {
		if (temp_resistance <= c_thermistor_info_table[i].resistance && 
			temp_resistance >= c_thermistor_info_table[i + 1].resistance) break;
	}
	
	if (i >= table_count - 1) {
		temperature_val = c_thermistor_info_table[table_count - 1].temperature; // last value
	}
	// resolving case when value lies between two resistances 
	else if (temp_resistance - c_thermistor_info_table[i + 1].resistance > (c_thermistor_info_table[i].resistance - c_thermistor_info_table[i + 1].resistance) / 2) {
		temperature_val = c_thermistor_info_table[i].temperature;
	}
	else {
		temperature_val = c_thermistor_info_table[i + 1].temperature;
	}
//	NRF_LOG_INFO("i = %d, temperature_val = %d\n", i, temperature_val);
	
	return temperature_val;
}


