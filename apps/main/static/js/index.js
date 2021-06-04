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
        show_likers: false,
        show_dislikers: false,
        post_display_id: 0,
        selection_done: false,
        show_upload: false,
        property_image: ""
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.complete = (rows) => {
        rows.map((row) => {
            row.thumbs_up = false;
            row.thumbs_down = false;
            row.likers = 0;
            row.dislikers = 0;
        });
    };

    app.search = function () {
        console.log("before if")
        if (app.vue.query.length >= 1) {
            console.log("before req");
            axios.get(search_url, {params: {q: app.vue.query, is_address: app.vue.show_address}})
                .then(function (response) {
                    let a = document.createElement('a');
                    a.href = response.data.url;
                    a.click();
                });
            console.log("after req");
        } else {
            app.vue.results = [];
        }
    };

    app.set_post_status = function (new_status) {
        app.vue.post_mode = new_status;
    };

    app.change_likers = function (status, id) {
        app.vue.show_likers = status;
        app.vue.post_display_id = id;
    }

    app.change_dislikers = function (status, id) {
        app.vue.show_dislikers = status;
        app.vue.post_display_id = id;
    }

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
                    console.log(app.vue.content_stars)

                    app.vue.rows.push({
                        id: response.data.id,
                        content: app.vue.add_content,
                        stars: parseInt(app.vue.content_stars),
                        property_manager_id: managerID,
                        name: response.data.name,
                        user_email: response.data.email,
                        day: response.data.day,
                    });
                    app.enumerate(app.vue.rows);
                    app.complete(app.vue.rows);
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

    app.toggle_show_upload = function(new_status) {
        app.vue.show_upload = new_status;
    }

    app.thumbs_change = async function (idx, idf) {
        let rating = 4;
        let post = app.vue.rows[idx];
        if(idf == 0){
            post.thumbs_up=true;
            if(post.thumbs_down==true){
                post.thumbs_down=false;
                post.dislikers = post.dislikers - 1
            }
            rating = 5;
            post.likers = post.likers + 1
            app.enumerate(app.vue.rows);
        } else if(idf==1){
            post.thumbs_up=false;
            post.likers = post.likers -1
            app.enumerate(app.vue.rows);
        } else if(idf == 2){
            post.thumbs_down=true;
            if(post.thumbs_up==true){
                post.thumbs_up=false;
                post.likers = post.likers -1
            }
            rating = 6;
            post.dislikers = post.dislikers + 1
            app.enumerate(app.vue.rows);
        } else if(idf==3){
            post.thumbs_down=false;
            post.dislikers = post.dislikers - 1
            app.enumerate(app.vue.rows)
        }
        axios.post(set_rating_url, {post_id: post.id, rating: rating, likers: post.likers, dislikers: post.dislikers});
        app.vue.set_post_status(true); 
        app.vue.set_post_status(false); 
    };

    // app.property_has_image = function (mid) {
    //     //TODO;
    //     let img_str = app.get_property_image(mid);
    //     return img_str.length !== 0;
    // };

    // app.get_property_image = function (mid) {
    //     //TODO;

    //     // if the image has already been set and it's non-blank, then don't do this

    //     let img_str = ""; // make this into a vue variable so it's reactive on upload; will also need to call this func from init and set to that vue var
    //     axios.get(get_property_image_url, {params: {mid: managerID}}).then(
    //         function(response){
    //             console.log(response);
    //             img_str = response.data.img_str;
    //         }
    //     );
    //     console.log(img_str);
    //     return img_str;
    // };

    app.upload_file = function (event, mid) {
        let input = event.target;
        let file = input.files[0];
        if (file) {
            let reader = new FileReader();
            reader.addEventListener("load", function (){
                axios.post(upload_property_image_url,
                {
                    mid: managerID,
                    property_image: reader.result
                })
                .then( function () {
                    //sets the local preview
                    app.vue.property_image = reader.result; 
                    Vue.set(this, "property_image", reader.result);
                    console.log(property_image);
                })
            });
            reader.readAsDataURL(file);
        }
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        search: app.search,
        toggle_address: app.toggle_address,
        propertyPage: app.propertyPage,
        set_post_status: app.set_post_status,
        add_post: app.add_post,
        thumbs_change: app.thumbs_change,
        change_likers: app.change_likers,
        change_dislikers: app.change_dislikers,
        toggle_show_upload: app.toggle_show_upload,
        // get_property_image: app.get_property_image,
        // property_has_image: app.property_has_image,
        upload_file: app.upload_file
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        axios.get(load_posts_url).then(function (response) {
            app.vue.rows = app.enumerate(response.data.rows);
            app.complete(app.vue.rows);
            // console.log(app.vue.rows);
            axios.get(load_search_results_url, {params: {q: query, is_address: is_address}}).then(function(response) {
                app.vue.manager_list = app.enumerate(response.data.manager_list);
            }).finally( function(response){
                console.log("HAPPENDINGF")
                for(let post of app.vue.rows) {
                    axios.get(get_rating_url, {params: {post_id: post.id}}).then((result) => {
                        if(result.data.rating == 4){
                            post.thumbs_up = false;
                            post.thumbs_down = false;
                        } else if(result.data.rating == 5){
                            console.log("YEEEE")
                            post.thumbs_up = true;
                            post.thumbs_down = false;
                        } else if(result.data.rating == 6){
                            post.thumbs_up = false;
                            post.thumbs_down = true;
                        }
                        post.likers = result.data.likers;
                        post.dislikers = result.data.dislikers;
                    }).then(() => {app.set_post_status(true); app.set_post_status(false);});
            }})
        });
        if (managerID!== undefined){
            console.log("HELLO IM LUCA DE ALFARROO");
            // let property_image = app.get_property_image(managerID);
            axios.get(get_property_image_url, {params: {mid: managerID}})
                .then(
                function(response){
                    console.log(typeof response.data.img_str);
                    if( typeof response.data.img_str === "string") {
                        console.log(response);
                        Vue.set(this, 'property_image', response.data.img_str);
                        app.vue.property_image = response.data.img_str;
                        console.log(app.vue.property_image);
                    }
                }
            );
        }
        console.log("INIT APP");
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
