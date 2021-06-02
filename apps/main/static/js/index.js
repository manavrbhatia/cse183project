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
        show_address: 1,
        post_mode: false,
        add_content: "",
        content_stars: "",
        managerID: -1,
        rows: [],
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

    app.set_post_status = function (new_status) {
        app.vue.post_mode = new_status;
    };

    app.reset_form = function () {
        app.vue.add_content = "";
        app.vue.content_stars = "";
    };

    app.add_post = function () {
        axios.post(add_post_url,
            {
                content: app.vue.add_content,
                stars: app.vue.content_stars,
                mid: managerID,
            }).then(
                function (response){
                    app.vue.rows.push({
                        id: response.data.id,
                        content: app.vue.add_content,
                        stars: app.vue.content_stars,
                        property_manager_id: managerID,
                        user_email: response.data.email,
                    });
                    app.enumerate(app.vue.rows);
                    app.reset_form();
                    app.set_post_status(false);
                });
    };

    app.propertyPage = function(id) {
        console.log(id);
        app.vue.managerID = id;
        console.log(app.vue.managerID);
        console.log(app.vue.rows);
        axios.post(property_url, 
            {
                mid: app.vue.managerID,
            }).then(
            function(response) { 
                let a = document.createElement('a');
                a.href = response.data.url;
                a.click();
            }
        );
    }

    app.toggle_address = function (new_status) {
        app.vue.show_address = new_status;
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        search: app.search,
        toggle_address: app.toggle_address,
        propertyPage: app.propertyPage,
        set_post_status: app.set_post_status,
        add_post: app.add_post,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        axios.get(load_search_results_url).then(function(response) {
            app.vue.manager_list = app.enumerate(response.data.manager_list);
            axios.get(load_posts_url).then(function (response) {
                app.vue.rows = app.enumerate(response.data.rows);
                console.log(app.vue.rows);
            });
        });
        console.log("INIT APP");
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
