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
        async onSubmit() {
            if (!this.name && !this.typ && !this.city) {
                alert('Es wurde keine Eingabe gemacht.')
            }
            const body = {
                name: this.name,
                type: this.type,
                city: this.city,
            }
            const response = await fetch('api/search', {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                },
                body: JSON.stringify(body)
            })
            const data = await response.json()
            console.log(data)
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