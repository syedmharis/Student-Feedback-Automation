import asyncio
from playwright.async_api import async_playwright, ElementHandle

async def submit_survey(RollNo, Password):
    async with async_playwright() as p:
        forms = 14
       

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigate to the login page
        await page.goto('http://erp.uit.edu:803/StudentPortalBeta/Login')

        # Fill out the login form
        await page.fill('#txtRegistrationNo_cs', RollNo)
        await page.fill('#txtPassword_m6cs', Password)

        # Submit the login form
        await page.click('#btnlgn')

        # Wait for the survey page to load
        await page.wait_for_selector('#kt_content')

        # Navigate to the survey Forms
        await page.goto('http://erp.uit.edu:803/studentportalbeta/survey/2')

        for i in range(5):

            # Wait for the form button to appear and click it
            await page.wait_for_selector('#ctl00_ContentPlaceHolder1_TgridSurvey')
            await page.click(f'#ctl00_ContentPlaceHolder1_TgridSurvey_ctl00_ctl{forms}_RadButton1')

            # Select the rating for each radio button
            radio_count = 1052
            for i in range(280, 296):
                radio_button = await page.wait_for_selector(f'#rdo{radio_count}')
                await radio_button.click()
                radio_count += 5
                await asyncio.sleep(0.5) # Add a delay of 0.5 second

            # Fill out the text input field
            txt_input = await page.wait_for_selector('#txt296')
            res1 = 'Sir is always enthusiastic and engaged in the subject matter, which makes it easy for me to stay focused and interested in the class. They also go out of their way to help students outside of class and are always available to answer questions or provide additional resources. Overall, their dedication and commitment to teaching have had a positive impact on my academic success.'
            await txt_input.fill(res1)
            await asyncio.sleep(1) # Add a delay of 1 second

            # Fill out the text input field
            txt_input = await page.wait_for_selector('#txt297')
            res2 = 'I believe that one area of improvement for faculty members could be to provide more detailed and structured feedback on assignments and assessments. Sometimes it can be difficult to understand how to improve without specific and constructive feedback. Additionally, providing more opportunities for students to ask questions and seek clarification can also be helpful in improving the learning experience.'
            await txt_input.fill(res2)
            await asyncio.sleep(1) # Add a delay of 1 second

            # Submit the form
            submit_button = await page.wait_for_selector('#btnSubmit')
            await submit_button.click()

            # Wait for the alert to appear and accept it
            alert = await page.wait_for_event('dialog')
            # Confirm that the results were submitted and display the text in the text input box.
            await asyncio.sleep(2)
            await alert.accept()          

            # Back to Portal
            Portal_button = await page.wait_for_selector('#btnbackToPortal')
            await Portal_button.click()

            # Wait for the success message
            await page.wait_for_selector('#ctl00_ContentPlaceHolder1_TgridSurvey')

            forms = forms+2

            

        # Close the browser
        await browser.close()

my_rollno = input("Enter your Roll No: ")
my_password = input("Enter your Password: ")
asyncio.run(submit_survey(my_rollno,my_password))
