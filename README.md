# EmotionGait

Le emozioni svolgono un ruolo importante nella nostra vita quotidiana, infatti influenzano il nostro benessere, le relazioni interpersonali, le decisioni che prendiamo e il modo in cui reagiamo alle situazioni in cui ci troviamo. Le emozioni possono variare molto e comprendere una vasta gamma di stati come la gioia, la tristezza, la rabbia, e molte altre.
L’obiettivo di questo lavoro è quello di capire se sia possibile individuare l’emozione provata da una persona dalla sua camminata. Il progetto, analizzando l’andatura di una persona, estrae alcune caratteristiche e in base a queste cerca di capire l’emozione che sta provando.


## Comandi per l'esecuzione del modello

1. Spostarsi nella cartella EmotionGait
1. conda env create -f EmotionWalkEnv.yml
2. cd python
3. python main.py [absolute_path_video] [absolute_path_xlsx] | python main.py [absolute_path_video]

Con il comando python main.py [absolute_path_video] [absolute_path_xlsx] eseguo la valdiation del modello in base ai vari gait e alle loro rispettive etichette, mentre con il comando python main.py [absolute_path_video] il modello mi restitusice una probabile emozione associata ai gait.

Per eseguire la validation del modello sul nostro test set bisogna eseguire il comando:  python main.py .../EmotionGait2/video/test .../EmotionGait2/sondaggi/responses_test.xlsx

Ese: python main.py /Users/angeloafeltra/Documents/GitHub/EmotionGait2/video/test /Users/angeloafeltra/Documents/GitHub/EmotionGait2/sondaggi/responses_test.xlsx


