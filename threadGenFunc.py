import bs4, requests, urllib.request, pyimgur, os, pyperclip
import itertools, threading, time, sys
import IPython, htmlCodeForJupyter


def parsePage(URL):
    webpage = requests.get(URL)
    bsPage = bs4.BeautifulSoup(webpage.text, 'html.parser')
    return bsPage


def replaceTags(element):
    replacements = {'<strong>': '[B]', '</strong>': '[/B]', '<ul>': '[/SIZE][LIST]\n', '</ul>': '[/LIST]\n\n[SIZE=15px]', '<ol><li>': '[/SIZE][LIST=1]\n[*]', '</li></ol>': '\n[/LIST]\n\n[SIZE=15px]', '</li><li>': '\n[*]', '<li><p>': '[*][SIZE=15px]', '</p></li>': '[/SIZE]\n', '<br/></p>': '\n\n', '<p>': '', '</p>': '\n\n'}
    if type(element) == str:
        for i, j in replacements.items():
            element = element.replace(i, j)
    elif type(element) == list:
        for k in range(len(element)):
            for i, j in replacements.items():
                element[k] = element[k].replace(i, j)
    return element


def getHeader(bsPage):
    findLeadTitle = bsPage.find("h1", {"class": "udlite-heading-xl clp-lead__title clp-lead__title--small"}).text.strip()
    findLeadHeadline = bsPage.find("div", {"class": "udlite-text-md clp-lead__headline"}).text.strip()
    findStars = bsPage.find("span", {"class": "udlite-heading-sm star-rating--rating-number--3lVe8"}).text.strip()
    findRating = '('+bsPage.find("div", {"class": "styles--rating-wrapper--5a0Tr"}).text.strip().split(' (')[1]
    findEnrolledStudents = bsPage.find("div", {"data-purpose": "enrollment"}).text.strip()
    findAuthor = bsPage.find("a", {"class": "udlite-btn udlite-btn-large udlite-btn-link udlite-heading-md udlite-text-sm udlite-instructor-links"}).text.strip()
    findAuthorURL = 'https://www.udemy.com'+bsPage.find("div", {"class": "udlite-heading-lg instructor--instructor__title--34ItB"}).a['href']
    HeaderStr = '[COLOR=rgb(250, 197, 28)][FONT=Arial][SIZE=26px][B][U]' + findLeadTitle + '[/U][/B][/SIZE][/FONT][/COLOR]\n'\
                '[COLOR=rgb(204, 204, 204)][SIZE=15px]'+findLeadHeadline+'[/SIZE][/COLOR]\n'\
                '[COLOR=rgb(250, 197, 28)][SIZE=15px]' + findStars + ' ' + '★'*round(float(findStars)) + '☆'*(5-round(float(findStars))) + '[/SIZE][/COLOR][SIZE=15px]  |  ' + findRating + '[/SIZE]' \
                '[SIZE=15px]  |  ' + findEnrolledStudents + '  |  Author: [/SIZE]' \
                '[URL='+findAuthorURL+'][COLOR=rgb(250, 197, 28)][SIZE=15px][U]' + findAuthor + '[/U][/SIZE][/COLOR][/URL]\n'
    return HeaderStr


def getWhatYouWillLearn(bsPage):
    whatYouWillLearnStr = '''[COLOR=rgb(250, 197, 28)][FONT=Arial][SIZE=26px][B][U]What you'll learn:[/U][/B][/SIZE][/FONT][/COLOR]\n[SPOILER="VIEW"]\n[List]\n'''
    findWhatYouWillLearn = bsPage.find_all("span", {"class": "what-you-will-learn--objective-item--ECarc"})
    for element in findWhatYouWillLearn:
        whatYouWillLearnStr += '[*][SIZE=15px]'+element.text+'[/SIZE]\n'
    whatYouWillLearnStr += '[/List]\n[/SPOILER]\n\n'
    return whatYouWillLearnStr


def getDuration(bsPage):
    durationStr = '''[COLOR=rgb(250, 197, 28)][FONT=Arial][SIZE=26px][B][U]Course Duration:[/U][/B][/SIZE][/FONT][/COLOR]\n[SPOILER="VIEW"]\n[SIZE=15px]'''
    findDuration = bsPage.find("span", {"class": "curriculum--content-length--1XzLS"})
    durationStr += findDuration.text.replace('\xa0', ' ')+'[/SIZE]\n[/SPOILER]\n\n'
    return durationStr


def getRequirements(bsPage):
    requirementsStr = '''[COLOR=rgb(250, 197, 28)][FONT=Arial][SIZE=26px][B][U]Requirements:[/U][/B][/SIZE][/FONT][/COLOR]\n[SPOILER="VIEW"]\n[List]\n'''
    findRequirements = bsPage.find("div", {"class": "ud-component--course-landing-page-udlite--requirements"}).find_all("div", {"class": "udlite-block-list-item-content"})
    for element in findRequirements:
        requirementsStr += '[*][SIZE=15px]'+element.text+'[/SIZE]\n'
    requirementsStr += '[/List]\n[/SPOILER]\n\n'
    return requirementsStr


def getDescription(bsPage):
    descriptionStr = '''[COLOR=rgb(250, 197, 28)][FONT=Arial][SIZE=26px][B][U]Description:[/U][/B][/SIZE][/FONT][/COLOR]\n[SPOILER="VIEW"]\n[SIZE=15px]\n'''
    findDescription = bsPage.find("div", {"data-purpose": "safely-set-inner-html:description:description"})
    descriptionWithTags = replaceTags(str(findDescription)[66:-6])
    descriptionStr += descriptionWithTags+'[/SIZE][/SPOILER]\n\n'
    return descriptionStr


def getWhoThisCourseIsFor(bsPage):
    whoThisCourseIsForStr = '''[COLOR=rgb(250, 197, 28)][FONT=Arial][SIZE=26px][B][U]Who this course is for:[/U][/B][/SIZE][/FONT][/COLOR]\n[SPOILER="VIEW"]\n[List]\n'''
    findWhoThisCourseIsFor = bsPage.find("ul", {"class": "styles--audience__list--3NCqY"})
    replacementsAlt = {'<li>': '[*][SIZE=15px]', '</li>': '[/SIZE]\n'}
    whoThisCourseIsForWithTags = str(findWhoThisCourseIsFor)[42:-5]
    for i, j in replacementsAlt.items():
        whoThisCourseIsForWithTags = whoThisCourseIsForWithTags.replace(i, j)
    whoThisCourseIsForStr += whoThisCourseIsForWithTags+'[/List]\n[/SPOILER]\n\n'
    return whoThisCourseIsForStr


def getCoursePage(courseURL):
    coursePageStr = '''[COLOR=rgb(250, 197, 28)][FONT=Arial][SIZE=26px][B][U]Source:[/U][/B][/SIZE][/FONT][/COLOR]\n[SPOILER="VIEW"]\n[SIZE=15px]'''
    coursePageStr += '[B][COLOR=rgb(250, 197, 28)]UDEMY[/COLOR][/B]: [URL=' + courseURL + '][COLOR=rgb(97, 189, 109)][U]' + courseURL + '[/U][/COLOR][/URL]'+ '[/SIZE]\n[/SPOILER]\n'
    return coursePageStr


def getDownloadURL(downloadURL):
    downloadURLStr = '''[HR][/HR]\n[COLOR=rgb(250, 197, 28)][FONT=Arial][SIZE=26px][B][U]Download:[/U][/B][/SIZE][/FONT][/COLOR]\n'''
    downloadURLStr += '[HIDEREACT=1,2,7,3,4,8,5,6][DOWNCLOUD]' + downloadURL + '[/DOWNCLOUD][/HIDEREACT]'
    return downloadURLStr


def getCourseImage(bsPage):
    findImage = bsPage.find("span", {"class": "intro-asset--img-aspect--1UbeZ"})
    courseImageURL = findImage.img['srcset'].split(', ')[1].split('.jpg?')[0] + '.jpg'
    urllib.request.urlretrieve(courseImageURL, "course-image.jpg")
    uploadedImageURL = uploadCourseImage('course-image.jpg')
    if os.path.exists('course-image.jpg'):
        os.remove('course-image.jpg')
    return '[IMG]' + uploadedImageURL + '[/IMG]\n[HR][/HR]\n'


def uploadCourseImage(courseImagePath):
    CLIENT_ID = "31172f8992ecc48"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(courseImagePath)
    return uploaded_image.link


def clipIt(givenStr):
    pyperclip.copy(givenStr)
    print('╔══╦'+'═' * 43 +'╗')
    print('╠══╣ BBCode has been copied to the clipboard!'+' '*2+'║')
    print('╠══╣ Go paste it wherever you want:)'+' '*11+'║')
    print('╚══╩'+'═' * 43 +'╝')
    print()

def startWait():
    t = threading.Thread(target=animate)
    t.start()


def animate():
    global taskdone
    taskdone = False
    for c in itertools.cycle(['[|]', '[/]', '[-]', '[\\]']):
        if taskdone:
            break
        sys.stdout.write('\rGetting Info from the course page ' + c)
        sys.stdout.flush()
        time.sleep(0.1)


def endWait():
    global taskdone
    taskdone = True
    print('\r', end='')


def clearOutput():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def makeGlobal(var1, var2):
    global jupyterCourseURL, jupyterDownloadLink
    jupyterCourseURL = var1
    jupyterDownloadLink = var2

def jupyterBool(TorF):
    global jupyter, inpCourseURL, inpDownloadLink
    jupyter = TorF
    if jupyter:
        inpCourseURL = jupyterCourseURL
        if isWebsite(inpCourseURL):
            if isUdemy(inpCourseURL):
                pass
            else:
                print('[Error] [Enter valid Udemy URL]')
                exit()
        else:
            print('[Error] [Enter valid URL]')
            exit()
        inpDownloadLink = jupyterDownloadLink
        if isWebsite(inpDownloadLink):
            pass
        else:
            print('[Error] [Enter valid URL]')
            exit()
    else:
        print('\033[H\033[J', end='')
        welcomeText()
        print('[Currently this tool only works with UDEMY URLs]')
        while True:
            inpCourseURL = input('Enter Course URL : ')
            if isWebsite(inpCourseURL):
                if isUdemy(inpCourseURL):
                    print('\033[H\033[J', end='')
                    print('Enter Course URL :', inpCourseURL)
                    break
                else:
                    print('\033[H\033[J', end='')
                    print('[Error] [Enter valid Udemy URL]')
            else:
                print('\033[H\033[J', end='')
                print('[Error] [Enter valid URL]')
        while True:
            inpDownloadLink = input('Enter Download Link : ')
            if isWebsite(inpDownloadLink):
                break
            else:
                print('\033[H\033[J', end='')
                print('[Error] [Enter valid URL]')
        print('\033[H\033[J', end='')


def isWebsite(website):
    try:
        if urllib.request.urlopen(website).getcode() == 200:
            return True
    except:
        return False


def isUdemy(website):
    if 'udemy.com/course/' in website:
        return True
    else:
        return False


def displayCode(markdownStr):
    bbCode = markdownStr
    if jupyter:
        IPython.display.display(IPython.display.HTML(htmlCodeForJupyter.styles))
        IPython.display.display(IPython.display.HTML(eval('f' + repr(htmlCodeForJupyter.body))))
        IPython.display.display(IPython.display.HTML(htmlCodeForJupyter.scripts))
    else:
        clipIt(bbCode)


def welcomeText():
    if os.name == 'nt':
        columns, lines = 60, 24
    else:
        columns, lines = os.get_terminal_size()
    welcomeTextList = '''
    ____  _            _    ____                 _
     | __ )| | __ _  ___| | _|  _ \ ___  __ _ _ __| |
     |  _ \| |/ _` |/ __| |/ / |_) / _ \/ _` | '__| |
     | |_) | | (_| | (__|   <|  __/  __/ (_| | |  | |
     |____/|_|\__,_|\___|_|\_\_|   \___|\__,_|_|  |_|
     ---- THREAD GENERATOR FOR TUTORIALS SECTION ----
     --------------- CREATED BY DUDU ----------------'''.split('\n')
    print('\n'*(int(lines/2)-6))
    for i in range(len(welcomeTextList[1:])):
        print(welcomeTextList[1:][i].center(columns-5))
    time.sleep(5)
    print('\033[H\033[J', end='')
