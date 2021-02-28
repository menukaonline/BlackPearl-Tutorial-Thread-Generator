import threadGenFunc

# courseURL = 'https://www.udemy.com/course/learn-javascript-online/'
# downloadURL = 'https://drive.google.com/file/d/1o7ngqzGJyW8LrQoqcazC3VjKu0b_o02Z/view?usp=sharing'
threadGenFunc.jupyterBool(False)
# threadGenFunc.makeGlobal(courseURL, downloadURL)
threadGenFunc.startWait()

coursePage = threadGenFunc.parsePage(threadGenFunc.inpCourseURL)
whatYouWillLearn = threadGenFunc.getWhatYouWillLearn(coursePage)
courseHeader = threadGenFunc.getHeader(coursePage)
courseDuration = threadGenFunc.getDuration(coursePage)
courseRequirements = threadGenFunc.getRequirements(coursePage)
courseDescription = threadGenFunc.getDescription(coursePage)
whoThisCourseIsFor = threadGenFunc.getWhoThisCourseIsFor(coursePage)
courseImage = threadGenFunc.getCourseImage(coursePage)
coursePage = threadGenFunc.getCoursePage(threadGenFunc.inpCourseURL)
downloadLink = threadGenFunc.getDownloadURL(threadGenFunc.inpDownloadLink)

threadGenFunc.endWait()

bbCode = courseHeader + courseImage + whatYouWillLearn + courseDuration + courseRequirements + courseDescription + whoThisCourseIsFor + coursePage + downloadLink

threadGenFunc.displayCode(bbCode)


# Name : Thread Generator for BlackPearl Tutorials Section
