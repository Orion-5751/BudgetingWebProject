var categories = {
    'Debt Payments': ['Credit Card Payments', 'Student Loans', 'Other Loans'],
    'Education': ['Books', 'Fees', 'Others', 'Supplies', 'Tuition'],
    'Entertainment': ['Concerts', 'Events', 'Gaming', 'Hobbies', 'Movies', 'Parties', 'Shopping', 'Sports', 'Subscriptions', 'Travel', 'Others'],
    'Food': ['Breakfast', 'Lunch', 'Dinner', 'Alcohol', 'Dining Out', 'Drinks', 'Groceries', 'Snacks', 'Others'],
    'Housing': ['Building Management', 'Cable', 'Furniture/Decorations', 'Internet/Data', 'Maintenance/Repairs', 'Rent/Mortgage', 'Utilities', 'Others'],
    'Insurance': ['Car Insurance', 'Health Insurance', "Homeowner's/Renter's Insurance", 'Life Insurance', 'Other Insurances'],
    'Miscellaneous': ['Donations', 'Gifts', 'Unexpected Expenses'],
    'Personal': ['Clothing', 'Cosmetics', 'Fitness', 'Haircut', 'Health', "Pets", 'Religion', 'Others'],
    'Savings/Investments': ['Emergency Fund', 'Retirement', 'Other Investments'],
    'Transportation': ['Fuel', 'Parking/Tolls', 'Public Transit', 'Travel', 'Uber/Lyft', 'Vehicle Maintenance/Repairs', 'Others']
};

let type_general = document.getElementById("type_general")
let type_specific = document.getElementById("type_specific")

function select_general(id) {
    type_general.value = id;
    type_specific.value = '';
    document.getElementById("demo_g").textContent = ('Selected: ' + type_general.value);
    document.getElementById("demo_s").textContent = ('Selected: ')
    create_specific();
}

/*
function select_specific(id) {
    type_specific.value = id;
    document.getElementById("demo_s").textContent = ('Selected: ' + type_specific.value);
}*/

function create_specific() {
    let specific = document.getElementById("specific");
    specific.innerHTML = '';
    // creating button element
    for (item in categories[type_general.value]){
        var assign = categories[type_general.value][item];
        console.log(assign);
        let button = document.createElement('BUTTON');
        button.type = 'button';
        button.className = 'list-group-item list-group-item-action'
        button.name = assign;
        button.id = assign;
        button.value = assign;
        button.textContent = assign;

        // appending button to div
        specific.appendChild(button);
    }

}

document.addEventListener("click", function(e) {
    var parent = document.getElementById('specific');

    if (e.target !== parent && parent.contains(e.target)) {
      type_specific.value = e.target.name;
      document.getElementById("demo_s").textContent = ('Selected: ' + type_specific.value);
    }
  });