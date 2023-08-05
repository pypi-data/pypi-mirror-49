import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {Routes} from "@angular/router";
// Import a small abstraction library to switch between nativescript and web
import {PeekModuleFactory} from "@synerty/peek-util-web";
// Import the default route component
import {DocdbComponent} from "./docdb.component";
// Import the required classes from VortexJS
import {
    TupleActionPushNameService,
    TupleActionPushOfflineService,
    TupleActionPushService,
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService
} from "@synerty/vortexjs";
// Import the names we need for the
import {
    docDbFilt,
    docDbObservableName,
    docDbTupleOfflineServiceName,
    docDbActionProcessorName
} from "@peek/peek_plugin_docdb/_private/PluginNames";
// Import the names we need for the
import {ViewDocComponent} from "./view-doc/view.component";

// Import the names we need for the



// Define the child routes for this plugin
export const pluginRoutes: Routes = [
    {
        path: 'view_doc',
        component: ViewDocComponent
    },
    {
        path: 'view_doc/:modelSetKey/:key',
        component: ViewDocComponent
    },
    {
        path: '',
        pathMatch: 'full',
        component: DocdbComponent
    }

];

// Define the root module for this plugin.
// This module is loaded by the lazy loader, what ever this defines is what is started.
// When it first loads, it will look up the routs and then select the component to load.
@NgModule({
    imports: [
        CommonModule,
        PeekModuleFactory.RouterModule,
        PeekModuleFactory.RouterModule.forChild(pluginRoutes),
        ...PeekModuleFactory.FormsModules,
    ],
    exports: [],
    providers: [
    ],
    declarations: [DocdbComponent, ViewDocComponent]
})
export class DocDbModule {
}
