<template>
	<div>
		<footer class="footer">
			<span>Developed by Silence & Befezdow 2k18</span>
		</footer>
		<div></div>
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
		background: #f8f9fa;
        padding: 15px;
	}
</style>