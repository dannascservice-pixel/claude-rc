# -*- coding: utf-8 -*-
"""
Roteiro do vídeo "Nietzsche — o homem que transcendeu e enlouqueceu".

Cada cena tem:
  text   -> narração (vira áudio via TTS)
  shots  -> lista de imagens (arquivos do Wikimedia Commons) mostradas em sequência
  card   -> (opcional) texto exibido na tela em vez de/por cima da imagem
"""

SCENES = [
    # ---------------------------------------------------------------- ABERTURA
    dict(
        id="01_turim",
        shots=["Gabinio.Torino- Palazzo Carignano, Piazza Carlo Alberto, Prospetto Col Monumento A Carlo Alberto 045B1.jpg"],
        chapter="Turim, janeiro de 1889",
        text=(
            "Turim, Itália. Janeiro de 1889. "
            "Um homem de bigode espesso e olhar cansado atravessa a Piazza Carlo Alberto. "
            "Segundo um relato que se tornaria lendário, ele vê um cocheiro chicoteando um cavalo. "
            "Corre até o animal, abraça seu pescoço... e desaba, chorando. "
            "Ele nunca mais voltaria a ser o mesmo. "
            "Esse homem havia acabado de escrever que Deus estava morto, "
            "que a moral era uma invenção dos fracos, "
            "e que o ser humano era apenas uma ponte para algo maior. "
            "Seu nome era Friedrich Nietzsche."
        ),
    ),
    dict(
        id="02_titulo",
        shots=["Edvard Munch - Friedrich Nietzsche - MM.M.00724 - Munch Museum.jpg"],
        title=True,
        text=(
            "Esta é a história do filósofo que tentou ir além do próprio homem, "
            "e que pagou por isso com a própria razão."
        ),
    ),
    # ---------------------------------------------------------------- INFÂNCIA
    dict(
        id="03_rocken",
        shots=["Röcken (Lützen), the birthplace of Friedrich Nietzsche.jpg",
               "Friedrich Nietzsche - 1864.jpg"],
        chapter="I. O filho do pastor",
        text=(
            "Nietzsche nasceu em 15 de outubro de 1844, na pequena aldeia de Röcken, na Prússia. "
            "Seu pai, Carl Ludwig, era pastor luterano. "
            "Quando Friedrich tinha apenas quatro anos, o pai morreu de uma doença no cérebro. "
            "Meses depois, morreu também o irmão caçula. "
            "O menino cresceu numa casa cheia de mulheres, de silêncio, e de Bíblia. "
            "Era tão sério e devoto que os colegas o chamavam de 'o pequeno pastor'."
        ),
    ),
    dict(
        id="04_schopenhauer",
        shots=["20040430040DR Schulpforte (Naumburg) Kloster Pforta Torhaus.jpg",
               "Arthur Schopenhauer by J Schäfer, 1859.jpg"],
        text=(
            "Brilhante, estudou na rigorosa escola de Pforta, e depois filologia clássica "
            "em Bonn e em Leipzig. Foi ali que, num sebo, encontrou um livro que mudaria tudo: "
            "O Mundo como Vontade e Representação, de Arthur Schopenhauer. "
            "Pela primeira vez, alguém dizia em voz alta o que ele sentia: "
            "que a vida é movida por uma vontade cega, e que o sofrimento está no centro da existência. "
            "A fé do pequeno pastor começava a ruir."
        ),
    ),
    # ---------------------------------------------------------------- BASILEIA / WAGNER
    dict(
        id="05_basileia",
        shots=["Friedrich Nietzsche-1872.jpg"],
        chapter="II. O professor prodígio",
        text=(
            "Em 1869, com apenas vinte e quatro anos, e antes mesmo de concluir o doutorado, "
            "Nietzsche foi nomeado professor da Universidade de Basileia, na Suíça. "
            "Um prodígio. O futuro parecia traçado: uma carreira acadêmica respeitável, tranquila, previsível."
        ),
    ),
    dict(
        id="06_wagner",
        shots=["Richard Wagner. Franz Hanfstaengl, München, 1871.jpg",
               "Tribschen-Wagner-Museum-mit-Pilatus.jpg"],
        text=(
            "Mas então ele conheceu Richard Wagner. "
            "O compositor era trinta e um anos mais velho, famoso, magnético. "
            "Na casa de Wagner, às margens do lago de Lucerna, Nietzsche encontrou um pai, "
            "um mestre, e uma causa: o renascimento da cultura alemã através da arte."
        ),
    ),
    dict(
        id="07_tragedia",
        shots=["Friedrich Nietzsche - Die Geburt der Tragödie aus dem Geiste der Musk. Leipzig, E. W. Fritzsch, 1872 - title page.jpg"],
        card=("Apolo", "a forma, a ordem, a razão", "Dionísio", "o êxtase, o caos, a embriaguez da vida"),
        text=(
            "Em 1872, publicou seu primeiro livro, O Nascimento da Tragédia. "
            "Nele, propôs que a grandeza dos gregos nascia da tensão entre duas forças. "
            "Apolo: a forma, a ordem, a razão. "
            "E Dionísio: o êxtase, o caos, a embriaguez da vida. "
            "Os colegas acadêmicos ficaram escandalizados. "
            "Mas Nietzsche havia encontrado o deus que o acompanharia até o fim: Dionísio."
        ),
    ),
    dict(
        id="08_ruptura",
        shots=["Nietzsche187a.jpg"],
        text=(
            "A amizade com Wagner, porém, não sobreviveu. "
            "Nietzsche passou a ver no mestre um ídolo vaidoso, nacionalista, "
            "que acabou se curvando ao cristianismo que ambos pareciam ter superado. "
            "O rompimento foi definitivo. E doeu como um luto. "
            "Ao mesmo tempo, seu corpo começava a desmoronar: "
            "enxaquecas que duravam dias, vômitos, uma visão cada vez mais fraca. "
            "Em 1879, aos trinta e quatro anos, ele abandonou a universidade com uma pequena pensão. "
            "O professor prodígio havia acabado."
        ),
    ),
    # ---------------------------------------------------------------- O ANDARILHO
    dict(
        id="09_andarilho",
        shots=["Caspar David Friedrich - Wanderer above the sea of fog.jpg",
               "Sils Nietzsche Haus.JPG"],
        chapter="III. O andarilho",
        text=(
            "Começaram então os dez anos mais solitários, e mais férteis, da sua vida. "
            "Nietzsche virou um andarilho. "
            "Passava os verões nos Alpes suíços, em Sils Maria, e os invernos no litoral, "
            "em Gênova, em Nice, e por fim em Turim. "
            "Vivia em quartos alugados, quase cego, caminhando sozinho por horas, "
            "e escrevendo em cadernos o que pensava enquanto andava."
        ),
    ),
    dict(
        id="10_eterno_retorno",
        shots=["Piz Surlej and landscape reflecting on Lake Silvaplana.jpg"],
        text=(
            "Em agosto de 1881, caminhando à beira do lago de Silvaplana, "
            "diante de uma enorme rocha em forma de pirâmide, ele teve a ideia que considerava a mais pesada de todas. "
            "E se tudo o que você viveu tivesse que se repetir, exatamente igual, infinitas vezes? "
            "Cada dor, cada alegria, cada instante. "
            "Você amaldiçoaria o demônio que lhe trouxesse essa notícia? "
            "Ou responderia: nunca ouvi nada mais divino? "
            "Ele chamou isso de eterno retorno. "
            "E a resposta que buscava tinha nome: amor fati. Amar o próprio destino. "
            "Não apenas suportar o que é necessário, mas amá-lo."
        ),
    ),
    dict(
        id="11_lou",
        shots=["Nietzsche paul-ree lou-von-salome188.jpg"],
        text=(
            "Em 1882, ele acreditou, por um breve momento, que não estaria mais sozinho. "
            "Conheceu Lou Salomé, uma jovem russa de inteligência deslumbrante. "
            "Os dois, junto com o amigo Paul Rée, sonharam em viver e estudar juntos. "
            "Nietzsche a pediu em casamento. Ela recusou. "
            "Dessa época restou esta fotografia estranha, que o próprio Nietzsche ajudou a encenar: "
            "Lou numa carroça, segurando um chicote, e os dois filósofos puxando-a como animais. "
            "A amizade terminou em amargura. E a solidão voltou, mais funda do que nunca."
        ),
    ),
    # ---------------------------------------------------------------- AS IDEIAS
    dict(
        id="12_deus_morto",
        shots=["Nietzsche1882.jpg"],
        chapter="IV. A morte de Deus",
        quote=("Deus está morto. Deus continua morto.\nE fomos nós que o matamos.", "A Gaia Ciência, 1882"),
        text=(
            "Foi nesse período que ele escreveu sua frase mais famosa, e mais mal compreendida. "
            "Na Gaia Ciência, um louco entra no mercado com uma lanterna acesa em pleno dia, e grita: "
            "Deus está morto. Deus continua morto. E fomos nós que o matamos. "
            "Nietzsche não estava comemorando. Estava fazendo um diagnóstico. "
            "A Europa já não acreditava de verdade em Deus, "
            "mas continuava vivendo sobre os valores que dependiam dele. "
            "Quando essa base desabasse, viria o niilismo: a sensação de que nada tem sentido. "
            "E a pergunta que ele deixou para nós é terrível: "
            "sem Deus, de onde virão nossos valores?"
        ),
    ),
    dict(
        id="13_zaratustra",
        shots=["Also sprach Zarathustra. Ein Buch für Alle und Keinen. In drei Theilen.jpg",
               "Nietzsche Schreibmaschine.JPG"],
        chapter="V. Além do homem",
        quote=("É preciso ter ainda caos dentro de si\npara dar à luz uma estrela dançante.", "Assim Falou Zaratustra"),
        text=(
            "A resposta veio em forma de poema profético: Assim Falou Zaratustra. "
            "Nele, o profeta desce da montanha para anunciar o Übermensch, o além-do-homem. "
            "O homem, diz Zaratustra, é uma corda estendida entre o animal e o além-do-homem. "
            "Uma corda sobre um abismo. "
            "O além-do-homem não é uma raça superior, nem um tirano. "
            "É aquele que, sem Deus e sem consolo, tem a coragem de criar os próprios valores, "
            "e de dizer sim à vida inteira, inclusive à dor. "
            "É preciso ter ainda caos dentro de si, escreveu ele, para dar à luz uma estrela dançante. "
            "O livro quase não vendeu. A quarta parte, ele precisou imprimir por conta própria: "
            "cerca de quarenta exemplares, distribuídos a poucos amigos."
        ),
    ),
    dict(
        id="14_abismo",
        shots=["Edvard Munch, friedrich nietzsche, litografia, 1906.jpg"],
        quote=("E se você olhar longamente para um abismo,\no abismo também olha para dentro de você.", "Além do Bem e do Mal, 1886"),
        text=(
            "Nos anos seguintes, vieram Além do Bem e do Mal e a Genealogia da Moral. "
            "Nietzsche arrancava a máscara da moral tradicional, "
            "mostrando que por trás de muitas virtudes se escondiam o ressentimento e a vontade de poder. "
            "Ele escreveu: quem luta com monstros deve cuidar para não se tornar um monstro. "
            "E se você olhar longamente para um abismo, o abismo também olha para dentro de você. "
            "Ele estava olhando há muito tempo."
        ),
    ),
    # ---------------------------------------------------------------- 1888
    dict(
        id="15_1888",
        shots=["PiazzaCarloAlbertoTorino.jpg"],
        chapter="VI. Dinamite",
        quote=("Eu não sou um homem.\nEu sou dinamite.", "Ecce Homo, 1888"),
        text=(
            "Em 1888, em Turim, algo mudou. "
            "O homem doente e melancólico de repente se sentiu leve, eufórico, invencível. "
            "Em poucos meses, escreveu numa velocidade assombrosa: "
            "O Caso Wagner, Crepúsculo dos Ídolos, O Anticristo, Nietzsche contra Wagner, "
            "e uma autobiografia chamada Ecce Homo, com capítulos intitulados "
            "Por que sou tão sábio, e Por que sou um destino. "
            "Ali ele escreveu: Eu não sou um homem. Eu sou dinamite. "
            "Era genialidade. Mas era também, talvez, o começo do fim."
        ),
    ),
    # ---------------------------------------------------------------- O COLAPSO
    dict(
        id="16_colapso",
        shots=["Gabinio.Torino- Palazzo Carignano, Piazza Carlo Alberto, Prospetto Col Monumento A Carlo Alberto, Vista Di Scorcio 045B4.jpg"],
        chapter="VII. O colapso",
        text=(
            "E então, no início de janeiro de 1889, aconteceu o colapso na praça de Turim. "
            "A história do cavalo talvez seja, em parte, lenda. Mas o que veio depois está documentado. "
            "Nos dias seguintes, Nietzsche enviou bilhetes delirantes a amigos, a Cosima Wagner, ao rei da Itália. "
            "Assinava como Dionísio. Ou como O Crucificado. "
            "Numa delas, escreveu que preferiria ser professor em Basileia a ser Deus, "
            "mas que não ousara levar seu egoísmo tão longe."
        ),
    ),
    dict(
        id="17_overbeck",
        shots=["Nietzsche Olde 01.JPG"],
        quote=("— Dionísio\n— O Crucificado", "assinaturas das cartas da loucura, janeiro de 1889"),
        text=(
            "Seu velho amigo Franz Overbeck correu de Basileia até Turim. Segundo os relatos, "
            "Nietzsche tocava piano com os cotovelos, cantava e dançava sozinho no quarto. "
            "Levou-o de volta à Suíça, e de lá ele foi internado numa clínica psiquiátrica em Jena. "
            "Nietzsche tinha quarenta e quatro anos. "
            "Nunca mais escreveria uma única linha filosófica."
        ),
    ),
    dict(
        id="18_silencio",
        shots=["Weimar, Museum Neues Weimar, Hans Olde, Friedrich Nietzsche auf dem Krankenbett.jpg",
               "Nietzsche Olde 08.JPG"],
        chapter="VIII. Onze anos de silêncio",
        text=(
            "Seguiram-se onze anos de silêncio. "
            "Primeiro sob os cuidados da mãe, em Naumburg. "
            "Depois, quando a mãe morreu, sob o controle da irmã, Elisabeth, "
            "que o levou para uma casa no alto de uma colina em Weimar, a Villa Silberblick. "
            "Ali, o homem que anunciou o além-do-homem passava os dias numa cadeira na varanda, "
            "olhando o vazio, quase sem falar. "
            "Enquanto isso, ironicamente, sua obra começava a ficar famosa em toda a Europa. "
            "Ele nunca soube."
        ),
    ),
    dict(
        id="19_elisabeth",
        shots=["Elisabeth Nietzsche.jpg", "Nietzsche-Archiv in der Villa Silberblick in Weimar.jpg"],
        text=(
            "Elisabeth transformou o irmão incapacitado num espetáculo. "
            "Recebia visitantes para vê-lo, criou o Arquivo Nietzsche, "
            "e controlou seus manuscritos. Ela havia sido casada com um militante antissemita, "
            "com quem tentou fundar uma colônia ariana no Paraguai. "
            "Nietzsche desprezava o antissemitismo, e se indignava abertamente com o cunhado por isso. "
            "Mas, depois da morte dele, Elisabeth montou a partir de anotações soltas "
            "um livro chamado A Vontade de Poder, e ajudou a vender a imagem de um Nietzsche "
            "nacionalista, que décadas depois seria explorada pelo nazismo. "
            "Foi talvez a maior traição já sofrida por um filósofo."
        ),
    ),
    dict(
        id="20_morte",
        shots=["Nietzsches Grab in Röcken (01).jpg"],
        text=(
            "Friedrich Nietzsche morreu em 25 de agosto de 1900, em Weimar, aos cinquenta e cinco anos. "
            "Foi enterrado em Röcken, ao lado do pai pastor, junto à igreja onde havia sido batizado. "
            "O homem que anunciou a morte de Deus repousa à sombra de uma igreja."
        ),
    ),
    # ---------------------------------------------------------------- O QUE CAUSOU
    dict(
        id="21_causa",
        shots=["Hans Olde Head Study of Friedrich Nietzsche Thielska 333a.tif"],
        chapter="IX. O que o enlouqueceu?",
        text=(
            "Mas afinal, o que enlouqueceu Nietzsche? "
            "Por quase um século, a explicação oficial foi a sífilis. "
            "Hoje, muitos estudiosos duvidam dela. "
            "Alguns médicos apontam para um tumor cerebral, outros para uma doença vascular hereditária, "
            "o que lembraria a morte precoce do pai, ou para uma forma de demência. "
            "A verdade é que não sabemos. "
            "E talvez a pergunta mais interessante não seja médica. "
            "É filosófica: um homem pode pensar o impensável sem pagar um preço?"
        ),
    ),
    # ---------------------------------------------------------------- TRANSCENDÊNCIA
    dict(
        id="22_transcendeu",
        shots=["Munch - Friedrich Nietzsche, 1905–1906, MM.M.00254.jpg"],
        chapter="X. O homem que transcendeu",
        text=(
            "Durante a vida, Nietzsche foi um fracasso: sem leitores, sem família, sem saúde, sem amor. "
            "Ele mesmo previu: alguns nascem póstumos. "
            "E nasceu. No século vinte, sua obra atravessou a filosofia, a psicologia, a literatura, a arte. "
            "Freud, Heidegger, Sartre, Camus, Foucault: todos beberam do seu abismo. "
            "Nietzsche não transcendeu por ter vencido o sofrimento. "
            "Transcendeu porque transformou o próprio sofrimento em pensamento. "
            "Enquanto o corpo apodrecia, ele escrevia sobre a alegria. "
            "Enquanto estava sozinho, escrevia sobre dizer sim à vida."
        ),
    ),
    dict(
        id="23_final",
        shots=["Caspar David Friedrich - Wanderer above the sea of fog.jpg"],
        quote=("Torna-te quem tu és.", "Friedrich Nietzsche"),
        text=(
            "Talvez sua loucura seja o preço de quem olha tempo demais para o abismo. "
            "Ou talvez seja apenas uma tragédia biológica, sem sentido nenhum. "
            "Mas Nietzsche nos deixou uma pergunta que continua ecoando: "
            "se você tivesse que viver a sua vida de novo, exatamente igual, para sempre... "
            "você a amaria? "
            "Torna-te quem tu és."
        ),
    ),
    dict(
        id="24_outro",
        shots=["Grabstätte von Friedrich Nietzsche in Röcken.jpg"],
        outro=True,
        text=(
            "Se esta história te fez pensar, deixe nos comentários: "
            "você aceitaria o eterno retorno? "
            "Inscreva-se no canal para mais mergulhos na filosofia. Até a próxima."
        ),
    ),
]
