import {Image, Nav} from "react-bootstrap";
import Logo from '../../images/logo.png';
import "./index.css"
import { FaHome, FaUsers } from 'react-icons/fa';
import { GiPoliceBadge } from "react-icons/gi";

const VerticalNavBar = () => {
    return (
        <Nav className="flex-column verticalNavBar" >
            <Image src={Logo} alt='iFooty'style={{width:'100px', height:'100px'}}></Image>
            <Nav.Link href="myteam">
                <FaHome style={{ marginRight: '8px' }} />
                My Team
            </Nav.Link>
            <Nav.Link href="players">
                <FaUsers style={{ marginRight: '8px' }} />
                Players
            </Nav.Link>
            <Nav.Link href="teams">
                <GiPoliceBadge style={{ marginRight: '8px' }} />
                Teams
            </Nav.Link>
        </Nav>
    );
};

export default VerticalNavBar;