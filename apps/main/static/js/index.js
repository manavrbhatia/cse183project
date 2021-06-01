// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        manager_list: [],
        query: "",
        results: [],
        show_address: 1
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.search = function () {
        console.log("before if")
        if (app.vue.query.length >= 1) {
            console.log("before req");
            axios.get(search_url, {params: {q: app.vue.query, is_address: 2}});
                // .then(function (result) {
                //     app.vue.results = result.data.results;
                // });
            console.log("after req");
        } else {
            app.vue.results = [];
        }
    };

    app.toggle_address = function (new_status) {
        app.vue.show_address = new_status;
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        search: app.search,
        toggle_address: app.toggle_address
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // axios.get(load_search_results_url, {params: {query=query}}).then(function(response) {
        //     app.vue.manager_list = app.enumerate(response.data.manager_list);
        // });
        console.log(app.vue.manager_list);
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
