# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s iuem20.studysite -t test_studysite.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src iuem20.studysite.testing.IUEM20_STUDYSITE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_studysite.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a studysite
  Given a logged-in site administrator
    and an add studysite form
   When I type 'My studysite' into the title field
    and I submit the form
   Then a studysite with the title 'My studysite' has been created

Scenario: As a site administrator I can view a studysite
  Given a logged-in site administrator
    and a studysite 'My studysite'
   When I go to the studysite view
   Then I can see the studysite title 'My studysite'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add studysite form
  Go To  ${PLONE_URL}/++add++studysite

a studysite 'My studysite'
  Create content  type=studysite  id=my-studysite  title=My studysite


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the studysite view
  Go To  ${PLONE_URL}/my-studysite
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a studysite with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the studysite title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
