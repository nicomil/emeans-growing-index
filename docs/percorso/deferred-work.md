- source_spec: `docs/percorso/spec-1-emeans-numpy-2d.md`
  summary: Misurare se azzerare le somme d'epoca dei cluster divisi, e saltare la rianimazione all'ultimo passo, migliora i centroidi finalizzati.
  evidence: Dopo una divisione, donatore e figlio continuano ad accumulare nelle somme dell'epoca i punti presi dalla posizione precedente, quindi la finalizzazione media due regioni diverse. Faiss 1.16.0 fa lo stesso; il revisore non ha osservato danni perché nei dati di prova le divisioni si esauriscono presto. Rilevante per la partenza a caldo, dove le divisioni possono avvenire anche tardi.
- source_spec: `docs/percorso/spec-3-partenza-a-caldo.md`
  summary: Aggiungere la strategia a caldo che legge solo i punti nuovi (o i nuovi più un campione dei vecchi), con costo proporzionale alla quota di dati nuovi.
  evidence: In exp_warm.py tutte le strategie rileggono l'intero insieme di dati. Il caso d'uso incrementale reale non è misurato, e senza di esso non si sa se la massa iniziale serva dove conta.
- source_spec: `docs/percorso/spec-3-partenza-a-caldo.md`
  summary: Ripetere l'esperimento su dati a gruppi netti, con abbastanza seed da reggere la varianza.
  evidence: La miscela sovrapposta è stata scelta dopo aver visto che i gruppi netti davano un riferimento instabile (4-8% tra seed). È il regime in cui contano i cluster senza centroide e la rianimazione, ed è stato escluso, non studiato.
- source_spec: `docs/percorso/spec-3-partenza-a-caldo.md`
  summary: Tenere fissi batch e passo tra le colonne, oppure aggiungere colonne di controllo, per separare l'effetto della deriva da quello della ricetta.
  evidence: La legge di scala dà batch 1024 e passo 0,25 / 0,23 al 5% e al 20%, batch 2048 e passo 0,34 al 50%. L'eccesso a caldo non è monotòno lungo le colonne (+1,05%, +1,85%, +0,12%).
- source_spec: `docs/percorso/spec-3-partenza-a-caldo.md`
  summary: Misurare l'errore separato su punti vecchi e nuovi, la stabilità dei cluster, e usare un riferimento a convergenza con seed distinti per dati e algoritmo.
  evidence: Il revisore misura, al 20%, 30,5 sui vecchi e 52,2 sui nuovi per i centroidi vecchi contro 31,3 e 32,6 a caldo; e un riferimento a 10 epoche migliore dello 0,25% di quello a 3. La stabilità è il motivo pratico per partire a caldo e non è misurata.
- source_spec: `docs/percorso/spec-4-solo-punti-nuovi.md`
  summary: Scegliere la massa iniziale da un segnale di deriva misurato sui soli punti nuovi (errore dei punti nuovi sui centroidi vecchi rispetto a quello tipico dei vecchi).
  evidence: La massa migliore va da 1-3 senza deriva a circa 0,1 con molta deriva. Il segnale vale +1-2% senza deriva e +45-72% con deriva. Senza una regola automatica la configurazione fissa peggiora i casi senza deriva.
- source_spec: `docs/percorso/spec-4-solo-punti-nuovi.md`
  summary: Estendere la griglia oltre i bordi (m sotto 0,03, s sopra 1) e raffinarla tra 0,1 e 1; aggiungere casi misti in cui parte dei punti nuovi viene dalla distribuzione vecchia.
  evidence: Il minimo cade sul bordo con il 5% di punti nuovi (s = 1) e con il 50% sui gruppi netti (m = 0,03). C'è un solo tipo di deriva.
- source_spec: `docs/percorso/spec-4-solo-punti-nuovi.md`
  summary: Provare una rianimazione che sconta la massa solo dei cluster che ricevono punti, o con soglia sui conteggi veri.
  evidence: La rianimazione di serie ricicla i cluster vecchi che non ricevono punti nuovi e costa fino a 30 punti di errore; spenta non permette di riallocare centroidi verso la zona nuova.
- source_spec: `docs/percorso/spec-4-solo-punti-nuovi.md`
  summary: Riferimento più solido per i dati a gruppi netti (migliore di più ripartenze o Lloyd fino a convergenza).
  evidence: Sui gruppi netti il riferimento a 10 epoche cambia dell'8-13% tra due seed dello stesso insieme di dati e viene battuto del 20% da una epoca a caldo.
- source_spec: `docs/percorso/spec-4b-regola-della-massa.md`
  summary: Provare un segnale di deriva per cluster o per quantili, al posto della media globale.
  evidence: Due scenari con lo stesso segnale medio (0,36) vogliono masse 0,02 e 0,5. Una tabella per scenario scelta sugli insiemi di taratura raggiunge l'oracolo, quindi il margine dipende dalla forma della regola e non dal rumore.
- source_spec: `docs/percorso/spec-4b-regola-della-massa.md`
  summary: Valutare la regola dalla quota su quote e livelli di deriva non usati nella taratura, con masse sotto 0,01 e griglia più fitta.
  evidence: Taratura e valutazione condividono i 15 scenari; in quattro casi la curva dell'errore scende ancora al bordo inferiore della griglia.
- source_spec: `docs/percorso/spec-d-aggiornamenti-in-sequenza.md`
  summary: Riassegnazione locale: dopo l'aggiornamento sui punti nuovi, rileggere e riassegnare solo le liste dei cluster il cui centroide si è spostato oltre una soglia.
  evidence: Con la metrica delle liste l'errore dei punti iniziali sale di 9,6-12,7% quando i centroidi si spostano (massa 0,2); riassegnando tutto la stessa strategia scende da +10,4% a +3,4%. Il costo si potrebbe limitare ai cluster toccati, come fanno SPFresh e Ada-IVF.
- source_spec: `docs/percorso/spec-d-aggiornamenti-in-sequenza.md`
  summary: Rimisurare i passi 4 e 4b con la metrica delle liste e, su un indice vero, con il recall a numero fisso di liste sondate.
  evidence: Quei passi usano solo la metrica che riassegna tutto. La metrica delle liste è un errore di quantizzazione e non dice quanto recall si perde.
