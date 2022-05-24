<template>
<div> 
    <div id="search">
        <form>
            <input type="text" />
            <input type="text" />
            <input type="text" />
            <button class="button" type="button"> Suche starten!</button>
        </form>
        
    </div>
    <div>
        
    </div>
</div>
    
</template>

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