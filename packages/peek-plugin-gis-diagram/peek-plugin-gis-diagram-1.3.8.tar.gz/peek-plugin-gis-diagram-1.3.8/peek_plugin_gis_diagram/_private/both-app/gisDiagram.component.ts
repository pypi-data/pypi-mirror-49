import {Component} from "@angular/core";
import {GisDiagramNavService} from "./gis-diagram-nav.service";
import {TitleService} from "@synerty/peek-util";

import {
    TupleDataOfflineObserverService,
    TupleSelector,
    ComponentLifecycleEventEmitter
} from "@synerty/vortexjs";

@Component({
    selector: 'plugin-gis-diagram',
    templateUrl: 'gisDiagram.component.web.html',
    moduleId: module.id
})
export class GisDiagramComponent extends ComponentLifecycleEventEmitter {

    constructor(private titleService:TitleService,
                private tupleDataObserver: TupleDataOfflineObserverService,
                private nav: GisDiagramNavService) {
        super();

        this.titleService.setTitle("GIS Diagram");

    }

    navToDiagram() {
        this.nav.toShowDiagram();
    }


}
