# Budgeting Web App
#### Video Demo:  <https://youtu.be/krAU3zzIQqo>
#### Description: This Web Application helps users manage their personal finances, such as budgeting, tracking expenses, incomes, and setting financial goals.

Its development involves: Python, JavaScript, HTML, Jinja, Flask, Bootstrap, SQLite, Werkzeug, and several other libraries.

## Web pages (HTML)
### layout.html
This provides the general base template of all the following web pages. It imports necessary frameworks(like Bootstrap 5), includes a main **navigation bar**, and scripts for the **calendar date picker**. Additionally, the displayed contents in the navigation bar change depending on whether the user is logged in or not. In the event of an **error**, a message appears below the navigation bar and above the page-specific content.


### Register
The *register* page allows users to register for their accounts with a **username** and a **password**. The password is **hashed**, and stored separately for each user.

### Log In
The *Log In* page logs in any existing users with their own **username** and **password**.

### Log Out
The *Log Out* page logs out the user, ending their session.

### Home
The *Home* page lets the user have an overview of their financial status such as **budgets**, **expenses**, **savings**, **incomes**, and **saving goals** with four main sections.

The **Current Period** section provides the user with their budget per period, the start date of the current period, the total expenses and incomes within this period, how much budget remains before hitting the limit of the current period, and how much money is saved in this period. It also shows the total savings the user has accumulated so far.

The **Expenses** section provides the user with a detailed table of the user's expenses within the current period. Each row in the table provides information about an individual expense, including details like the date of the expense, category of the expense, price, and any repeating pattern if applicable.

The **Incomes** section, similar to the **Expenses** section, provides the user with a detailed table of the user's income within the current period. Each row in the table provides information on an individual income, including details like the date of the income, type, amount, and any repeat pattern if applicable.

The **Goals** section provides the user with an outlook on their savings goals. Each goal is represented as a progress bar that indicates the current saving status towards achieving the goal. For each goal, it shows the name of the item and the target amount to be saved.


### Set Budget
The *Set Budget* page first displays the user's **set budget**, and then a **form** for the user to **update** their **budgeting period**, **budget amount**, and a **starting date**. The selection of a budgeting period is done with a drop-down menu, with its options generated dynamically based on the "periods" variable passed to the template. The budget amount is done via an input field, limiting the amount to have a minimum value of 0 and a step value of 0.01 as how currencies are typically displayed. The starting date is determined by the user using a date picker. The date is displayed in "yyyy-mm-dd" format, and the input field is read-only to ensure that users pick a valid, existing date. At the end of the form, there is a submit button to submit the form and update the user's budget, which is stored in a SQLite database.

### Saving Goals
The *Saving Goals* page first provides the user with a detailed table of the user's **saving goals**. Each row in the table provides information on an individual goal, including details like the **name of the item**, the **amount/cost**, and the anticipated **deadline** to achieve that saving goal. Following the table, there is a **form** that prompts the user for a new entry of a new saving goal, containing the **name of the item**, the **amount/cost**, and the anticipated **deadline**. The form first consists of an input field for the item name and another input field for the amount/cost. It restricts the amount/cost to have a minimum value of 0 and a step value of 0.01 as how currencies are typically displayed. The anticipated deadline is determined by the user using a date picker. The date is displayed in "yyyy-mm-dd" format, and the input field is read-only to ensure that users pick a valid, existing date. At the end of the form, there is a submit button to submit the form and insert the **new saving goal** into the SQLite database.

### Expenses
The *Expenses* page first provides the user with a **form** to enter any recent purchases they have made. The form first consists of a date picker for the purchase **date**, an input field for the **price**, two options for one **general category** and one **specific category** of the expense, and two optional fields for specifying how many times the expense **repeats** itself and over a selected **period**. The date is determined by the user using a date picker. The date is displayed in "yyyy-mm-dd" format, and the input field is read-only to ensure that users pick a valid, existing date. The input field for the price restricts the entered price to have a minimum value of 0 and a step value of 0.01 as how currencies are typically displayed. On the left of the page, there is a **list of general expense categories**, each represented as a button. Clicking on a button triggers a JavaScript function, "select_general", which modifies the selected input for the general category and populates a **list of specific expense categories** accordingly on the right part of the page. At the end of the form, there is a submit button to submit the form and insert the new purchase into the SQLite database.

Following the form, there is a detailed table of all the purchases the user has made. Each row in the table provides information about an **individual purchase**, including details like the date the purchase was made, the general and specific category the purchase falls into, the price, and any repeating pattern if applicable.

### Income
The *Income* page, similar to the *Expenses* page, first provides the user a form to enter any recent income. The form first consists of a date picker for the **date**, an input field for the **amount earned**, a list group for the selection of a **type of income**, and two optional fields for specifying how many times the income **repeats** itself and over a selected **period**. The date is determined by the user using a date picker. The date is displayed in "yyyy-mm-dd" format, and the input field is read-only to ensure that users pick a valid, existing date. The input field for the income amount restricts the entered amount to have a minimum value of 0 and a step value of 0.01 as how currencies are typically displayed. A **list group of income types**, each represented as a button, modifies the selected input for the income type when clicked. At the end of the form, there is a submit button to submit the form and insert the new income entry into the SQLite database.

Following the form, there is a detailed table of all incomes the user has made. Each row in the table provides information about an **individual income**, including details like the date, the category that the income falls into, the amount earned, and any repeating pattern if applicable.

### Python, JavaScript, and CSS
Those files ensure the operational fluidity of the system. Python manages the backend processes which include ensuring **proper data inputs**, accessing, fetching, and updating the **SQLite database** as well as calculating the start date of the **current budgeting period**. JavaScript serves as a complement to the HTML structure, mainly working as the **select functions**. CSS is employed to **customize the aesthetics** of the web pages.

