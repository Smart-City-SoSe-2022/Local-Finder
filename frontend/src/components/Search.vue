<template>
<div> 
    <div id="search">
        <form>
            <input type="text" v-model="name" name="name" placeholder="Lokalname..."/>
            <input type="text" v-model="type" name="type" placeholder="Lokaltyp..."/>
            <input type="text" v-model="city" name="city" placeholder="Stadt..." />
            <button class="button" type="button" @click="onSubmit()"> Suche starten!</button>
        </form>
        
    </div>
    <div>
        
    </div>
</div>
    
</template>

<script>
export default {
    name: 'UserReg',
    data() {
        return {
            name: '',
            type: '',
            city: '',
        }
    },
    methods: {
        onSubmit() {
            var route = "/results?"
            if (this.name) {route += "name="+this.name} else {route += "name="}
            if (this.type) {route += "&type="+this.type} else {route += "&type="}
            if (this.city) {route += "&city="+this.city} else {route += "&city="}
            //this.$router.push({ name: 'Results', query: { name: this.name, city: this.city, type: this.type }})
            window.location.href = route
            
        }
    }
};
</script>

<style scoped>
    #search {
        background: #ddf;
        border-radius: 10px;
        padding: 10px 0;
    }
    form {
        
        margin: 0 auto;
    }
    form > input {
        display: block;
        min-width: 35ch;
        margin: 10px auto; 
        padding: 5px 10px;
        font-size: 2ch;
        border: 2px solid #ddf;
        border-radius: 10px;
    }

    form > input:focus {
        border: 2px solid black;
    }
</style>