import {CommonModule} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {NgModule} from "@angular/core";
import {Routes, RouterModule} from "@angular/router";
import {EditDiagramGenericMenuComponent} from "./edit-diagram-generic-menu-table/edit.component";
import {EditSettingComponent} from "./edit-setting-table/edit.component";


// Import our components
import {DiagramGenericMenuComponent} from "./diagramGenericMenu.component";

// Define the routes for this Angular module
export const pluginRoutes: Routes = [
    {
        path: '',
        component: DiagramGenericMenuComponent
    }

];

// Define the module
@NgModule({
    imports: [
        CommonModule,
        RouterModule.forChild(pluginRoutes),
        FormsModule
    ],
    exports: [],
    providers: [],
    declarations: [DiagramGenericMenuComponent, EditDiagramGenericMenuComponent, EditSettingComponent]
})
export class DiagramGenericMenuModule {

}
