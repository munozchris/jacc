Database README

SCHEMA - evals.db
---------------------------
Tables: 
e_xTA (general eval for classes without a TA)
e_oTA (general eval for classes with TA)
e_lang (general eval for language classes)
e_bio (eval for biology classes)

Table structures
---------------------------
e_xTA = "CREATE TABLE e_xTA(\n\
        EvalType TEXT,\n\
        CourseName TEXT,\n\
        CourseNum INT(10000),\n\
        CourseSection TEXT,\n\
        Dept VARCHAR(4),\n\
        Year INT(4),\n\
        Professors TEXT,\n\
        NumResponses INT(1000),\n\
        MaxHrs REAL,\n\
        MedHrs REAL,\n\
        MinHrs REAL,\n\
        YesReasonableCourseCount INT(1000),\n\
        NotReasonableCourseCount INT(1000),\n\
        DesireToTakeCourse TEXT,\n\
        TopReasonToTakeClass TEXT,\n\
        HowFrequentlyAssignmentsDue TEXT,\n\
        Instr_AccessibleOutsideClass TEXT,\n\
        Instr_EffectiveLecturer TEXT,\n\
        Instr_InterestingLecture TEXT,\n\
        Instr_Organized TEXT,\n\
        Instr_PositiveTowardStudents TEXT,\n\
        Instr_Recommendable TEXT,\n\
        InstructorStrengthsComments TEXT,\n\
        InstructorWeaknessesComments TEXT,\n\
        CourseAspectsToChange TEXT,\n\
        CourseAspectsToRetain TEXT);"

    e_oTA = "CREATE TABLE e_oTA(\n\
        EvalType TEXT,\n\
        CourseName TEXT,\n\
        CourseNum INT(10000),\n\
        CourseSection TEXT,\n\
        Dept VARCHAR(4),\n\
        Year INT(4),\n\
        Professors TEXT,\n\
        NumResponses INT(1000),\n\
        MaxHrs REAL,\n\
        MedHrs REAL,\n\
        MinHrs REAL,\n\
        YesReasonableCourseCount INT(1000),\n\
        NotReasonableCourseCount INT(1000),\n\
        DesireToTakeCourse TEXT,\n\
        TopReasonToTakeClass TEXT,\n\
        AppropriateCourseExpectations TEXT,\n\
        AppropriateLevelContent TEXT,\n\
        FairAssignmentGrading TEXT,\n\
        Instr_AccessibleOutsideClass TEXT,\n\
        Instr_EffectiveLecturer TEXT,\n\
        Instr_Engaging TEXT,\n\
        Instr_HelpfulOfficeHours TEXT,\n\
        Instr_Organized TEXT,\n\
        Instr_RespondedWellToQuestions TEXT,\n\
        LectureandDiscussionPreparesStudentsForAssignments TEXT,\n\
        StudentExpectationsMet TEXT,\n\
        StudentInsightGain TEXT,\n\
        StudentSkillsGained TEXT,\n\
        TimelyAssigmentGradingandFeedback TEXT);"

    e_bio = "CREATE TABLE e_bio(\n\
        EvalType TEXT,\n\
        CourseName TEXT,\n\
        CourseNum INT(10000),\n\
        CourseSection TEXT,\n\
        Dept VARCHAR(4),\n\
        Year INT(4),\n\
        Professors TEXT,\n\
        AppropriatenessScore REAL,\n\
        EducativeScore REAL,\n\
        CourseOrganizationScore REAL,\n\
        OverallClassRating REAL,\n\
        PriorExposureScore REAL,\n\
        MaxHrs REAL,\n\
        MedHrs REAL,\n\
        MinHrs REAL,\n\
        NumResponses INT(10000));"

    e_lang = "CREATE TABLE e_lang(\n\
        EvalType TEXT,\n\
        CourseName TEXT,\n\
        CourseNum INT(10000),\n\
        CourseSection TEXT,\n\
        Dept VARCHAR(4),\n\
        Year INT(4),\n\
        Professors TEXT,\n\
        NumResponses INT(1000),\n\
        MaxHrs REAL,\n\
        MedHrs REAL,\n\
        MinHrs REAL,\n\
        YesReasonableCourseCount INT(1000),\n\
        NotReasonableCourseCount INT(1000),\n\
        DesireToTakeCourse TEXT,\n\
        TopReasonToTakeClass TEXT,\n\
        Instr_AccessibleOutsideClassandHelpfulRating TEXT,\n\
        Instr_ConveyedLanguageSubtletiesRating TEXT,\n\
        Instr_EncouragedLanguageConversationRating TEXT,\n\
        Instr_FeedbackWasHelpfulRating TEXT,\n\
        OverallGoodInstructorYesCount INT(4),\n\
        OverallGoodInstructorNoCount INT(4),\n\
        StudiedLanguageBefore TEXT,\n\
        LanguageGrammarEmphasizedandStudied TEXT,\n\
        LanguageReadingEmphasizedandStudied TEXT,\n\
        LanguageSpeakingEmphasizedandStudied TEXT,\n\
        LanguageSpellingEmphasizedandStudied TEXT,\n\
        LanguageVocabEmphasizedandStudied TEXT,\n\
        LanguageWritingEmphasizedandStudied TEXT,\n\
        YesImprovedLanguageSkillsCount INT(4),\n\
        NoImprovedLanguageSkillsCount INT(4),\n\
        WouldRecommendClassCount INT(4),\n\
        WouldNotRecommendClassCount INT(4));"

################################

SCHEMA - courses.db
---------------------------
Tables:

CourseInfo (holds all basic class information)
SectionInfo (holds all section logistic information)
ProfTable (holds information on Professor)
DescTable (holds class description information)
---------------------------
Table structures:

CourseInfo = "CREATE TABLE CourseInfo(\n\
        CourseId INT(10000) Primary Key,\n\
        Dept VARCHAR(4),\n\
        CourseNum TEXT,\n\
        Title TEXT,\n\
        EvalLinks TEXT,\n\
        TotalEnroll INT(10),\n\
        CurrentTotalEnroll INT(10),\n\
        StartDate VARCHAR(15),\n\
        EndDate VARCHAR(15));"

SectionInfo = "CREATE TABLE SectionInfo(\n\
        SectionId INT(10000) Primary Key,\n\
        CourseId INT(10000),\n\
        Sect TEXT,\n\
        Professor TEXT,\n\
        Days1 VARCHAR(100),\n\
        Days2 VARCHAR(100),\n\
        StartTime1 INT,\n\
        StartTime2 INT,\n\
        EndTime1 INT,\n\
        EndTime2 INT,\n\
        SectionEnroll INT(10),\n\
        CurrentSectionEnroll INT(10));"


ProfTable = "CREATE TABLE ProfTable(\n\
        Professor VARCHAR(1000),\n\
        CourseId INT(10000),\n\
        SectionId INT(1000));"


DescTable = "CREATE TABLE Description(\n\
        CourseId INT(10000),\n\
        Description TEXT);"