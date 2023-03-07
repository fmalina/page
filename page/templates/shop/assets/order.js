// save form data to local storage
const OrderData = {
    form: document.getElementById("order_form"),
    save() {
        // Get all the form fields
        const fields = OrderData.form.querySelectorAll("input, select, textarea");
        // Create an object to store the form data
        const formData = {};
        // Iterate through the fields
        fields.forEach(field => {
            // Add the field name and value to the formData object
            formData[field.name] = field.value;
        });
        // Save the formData object to local storage
        localStorage.setItem("formData", JSON.stringify(formData));
    },

    load() {
        // Get the saved form data from local storage
        const savedData = localStorage.getItem("formData");
        // If there is saved data
        if (savedData) {
            // Parse the JSON string to an object
            const formData = JSON.parse(savedData);
            // Iterate through the formData object
            for (const field in formData) {
                // Get the form field by its name
                const formField = OrderData.form.elements[field];
                // If the form field exists
                if (formField) {
                    // Set the value of the form field to the saved value
                    formField.value = formData[field];
                }
            }
        }
    },

    validate(event) {
        const fields = ['name', 'address', 'postcode', 'country', 'phone', 'email'];
        let isvalid = true;

        for (const field of fields) {
            let section = document.getElementById(`${field}-section`);
            if (OrderData.form[field].value === '') {
                section.classList.add('error');
                event.preventDefault();
            } else {
                section.classList.remove('error');
            }
        }
        OrderData.prep(event);
        // event.preventDefault();
    },

    // Write order letter/email and cart into hidden fields
    prep(event) {
        const lang = Config[Config.lang];
        var o = '';
        for (const e of OrderData.form.elements) {
            if (e.value && e.name !== 'cartdata' && e.name !== 'orderletter') {
                o += `${lang[e.name]}: ${e.value}\n`;
            }
        }

        o += '\n<b>' + `${lang.order}</b>\n`;
        for (const item of Cart.items) {
            o += `${item.name} [${item.id}]\n`;
            o += `${Config.currency} ${item.price}\n`;
            o += `x ${item.quantity}ks\n\n`;
        }

        const cartdata = JSON.stringify(Cart.items);
        // const cartInput = document.getElementById('cartdata');
        const letterInput = document.getElementById('orderletter');
        // cartInput.value = cartdata;
        letterInput.value = o;

        console.log(o)
    }
}


window.addEventListener("load", OrderData.load);
window.addEventListener("load", CartData.load);

OrderData.form.addEventListener("submit", OrderData.validate);
OrderData.form.addEventListener("submit", OrderData.save);
