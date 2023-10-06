# 문제3. 무음 구간 찾기

1. requirements.txt
	pydub
	json
	tqdm
	os

2. how to start
	python .\Q3.py --pcm_list .\pcmlist.txt --output_file .\..\..\output\Q3.json --thresholds '{\"task3_01.pcm\": 142,\"task3_02.pcm\": 9,\"task3_03.pcm\": 773,\"task3_04.pcm\": 3000,\"task3_05.pcm\": 3390}'
	thresholds = {
		"task3_01.pcm": 142,
		"task3_02.pcm": 9,
		"task3_03.pcm": 773,
		"task3_04.pcm": 3000,
		"task3_05.pcm": 3390,
	}