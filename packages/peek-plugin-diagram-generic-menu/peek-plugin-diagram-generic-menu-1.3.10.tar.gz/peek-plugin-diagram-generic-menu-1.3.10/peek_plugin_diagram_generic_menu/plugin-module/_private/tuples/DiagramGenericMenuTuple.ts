import {addTupleType, Tuple} from "@synerty/vortexjs";
import {diagramGenericMenuTuplePrefix} from "../PluginNames";


@addTupleType
export class DiagramGenericMenuTuple extends Tuple {
    public static readonly tupleName = diagramGenericMenuTuplePrefix + "DiagramGenericMenuTuple";

    //  Description of date1
    id : number;

    modelSetKey : string | null;
    coordSetKey : string | null;
    faIcon : string | null;
    title : string;
    url : string;

    constructor() {
        super(DiagramGenericMenuTuple.tupleName)
    }
}