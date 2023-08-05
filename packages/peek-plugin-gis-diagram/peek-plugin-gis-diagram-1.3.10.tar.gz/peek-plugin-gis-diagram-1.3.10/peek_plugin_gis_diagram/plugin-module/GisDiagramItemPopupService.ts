import {Injectable, Optional} from "@angular/core";
import {Router} from "@angular/router";
import {Observable} from "rxjs/Observable";
import {Subject} from "rxjs/Subject";
import {
    DiagramItemPopupContextI,
    DiagramItemPopupService
} from "@peek/peek_plugin_diagram/DiagramItemPopupService";
import {gisDiagramModelSetKey} from "./_private/PluginNames";

import {
    DocDbDocumentTypeTuple,
    DocDbPropertyTuple,
    DocDbService,
    DocumentResultI,
    DocumentTuple
} from "@peek/peek_plugin_docdb";

import {
    SearchObjectTypeTuple,
    SearchResultObjectTuple,
    SearchService
} from "@peek/peek_core_search";

export {
    DiagramItemPopupContextI
}from "@peek/peek_plugin_diagram/DiagramItemPopupService";

/** Gis Diagram Item Popup Service
 *
 * This service allows other plugins to add information to the item select popups.
 *
 * This is a helper service to simplify integrations with the diagram.
 *
 */
@Injectable()
export class GisDiagramItemPopupService {

    private _subject = new Subject<DiagramItemPopupContextI>();

    constructor(private router: Router,
                private diagramService: DiagramItemPopupService,
                private searchService: SearchService,
                private docDbService: DocDbService) {
        this.diagramService
            .itemPopupObservable()
            .subscribe((context: DiagramItemPopupContextI) => {
                if (context.modelSetKey != gisDiagramModelSetKey)
                    return;
                this.addDisplayDetails(context);
                this.addDocDetails(context);
                this.addSearchRoutes(context);
                this._subject.next(context);
            });

    }

    /** Item Popup Observable
     *
     * This method returns an observer for this coordSetKey, that is fired when the item
     * is selected.
     */
    itemPopupObservable(): Observable<DiagramItemPopupContextI> {
        return this._subject;
    }

    private addDisplayDetails(context: DiagramItemPopupContextI): void {
        if (context.data["alias"] == null)
            return;

        context.addDetailItems(
            [{
                title: "Alias",
                value: context.data["alias"]
            },
                {
                    title: "Name",
                    value: context.data["name"]
                }]
        );

    }

    private addDocDetails(context: DiagramItemPopupContextI): void {
        if (context.key == null)
            return;

        this.docDbService.getObjects("pofDiagram", [context.key])
            .then((docs: DocumentResultI) => {
                let doc = docs[context.key];
                if (doc == null) {
                    console.log(`Document ${context.key} can not be found.`);
                    return;
                }

                let docProps = this.docDbService.getNiceOrderedProperties(doc);
                context.addDetailItems(docProps);
            });


    }

    private addSearchRoutes(context: DiagramItemPopupContextI): void {
        if (context.key == null)
            return;


        this.searchService
            .getObjects('key', null, context.key)
            .then((results: SearchResultObjectTuple[]) => {
                if (results.length == 0)
                    return;

                let searchObject = results[0];
                for (let route of searchObject.routes) {
                    // // If the link is to this
                    // if (route.path.indexOf('peek_plugin_pof_diagram') != -1)
                    //     continue;
                    // Show the menu option
                    context.addMenuItem({
                        name: route.title,
                        tooltip: null,
                        icon: 'search',
                        callback: () => route.navTo(this.router),
                        children: []
                    });
                }
            });

    }


}