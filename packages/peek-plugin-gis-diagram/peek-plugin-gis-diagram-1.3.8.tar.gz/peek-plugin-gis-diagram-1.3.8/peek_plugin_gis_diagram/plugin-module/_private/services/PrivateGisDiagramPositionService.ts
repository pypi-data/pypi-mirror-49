import {GisDiagramPositionService} from "../../GisDiagramPositionService";
import {Injectable} from "@angular/core";
import {PrivateGisDiagramNavService} from "./private-gis-diagram-nav.service";
import {DiagramPositionService} from "@peek/peek_plugin_diagram/DiagramPositionService";
import {gisDiagramModelSetKey} from "../PluginNames";

/** Gis Diagram Position Service
 *
 * This service allows other plugins to integrate with the Gis Diagram.
 *
 * This service is a root, persistently provided services, so an plugin need only call
 * "position", this service then loads the diagram and then positions it.
 *
 */
@Injectable()
export class PrivateGisDiagramPositionService extends GisDiagramPositionService {

    constructor(private nav: PrivateGisDiagramNavService,
                private pos: DiagramPositionService) {
        super();

    }

    positionByKey(dispKey: string): void {
        this.pos.isReadyObservable()
            .first()
            .subscribe(() => {
                this.pos.positionByKey(gisDiagramModelSetKey, null, {
                    highlightKey: dispKey
                });
            });

        this.nav.toShowDiagram();

    }


    canPositionByKey(dispKey: string): Promise<boolean>  {
        return this.pos.canPositionByKey(gisDiagramModelSetKey, dispKey);
    }


}