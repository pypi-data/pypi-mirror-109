const preload = () => import('./wizard-dialog-8dd8d654.js');
const startWizard = async () => {
    preload();
    document.body.append(document.createElement("esphome-wizard-dialog"));
};
const attachWizard = () => {
    document.querySelectorAll("[data-action='wizard']").forEach((btn) => {
        btn.addEventListener("click", startWizard);
        btn.addEventListener("mouseover", preload, { once: true });
    });
};

console.log("New frontend handlers installed");
attachWizard();
