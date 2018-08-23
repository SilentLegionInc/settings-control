<template>
	<div>
		<footer class="footer">
			<span>Developed by Silence & Befezdow 2k18</span>
		</footer>
	</div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    @Component
    export default class Footer extends Vue {}
</script>

<style scoped>
	.footer {
		text-align: center;
		background-color: #6f7bbf;
        padding: 15px;
	}
</style>