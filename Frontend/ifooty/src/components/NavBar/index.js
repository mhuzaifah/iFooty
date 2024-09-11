import {Container, Image, Nav} from "react-bootstrap";
import {useState} from "react";
import Logo from '../../images/logo.png';
import Club from '../../images/clubsHero.png';
import "./index.css"
import { FaHome, FaUsers } from 'react-icons/fa';
import { GiPoliceBadge } from "react-icons/gi";
import {Link, useLocation} from "react-router-dom";

const VerticalNavBar = () => {

    const location = useLocation();
    const [activeNavOption, setActiveNavOption] = useState(location.pathname.replace("/",""));

    const handleSelect = (selectedNavOption) => {
        setActiveNavOption(selectedNavOption);
    }

    const navOptions = [
        { title:"My Team", link:"myteam", icon:<FaHome className="navIcon" />},
        { title:"Teams", link:"teams", icon:<FaUsers className="navIcon" />},
        { title:"Players", link:"players", icon:<GiPoliceBadge className="navIcon" />},
    ]

    return (
        <Nav className="verticalNavBar flex-column" >
            <Image src={Logo} alt='iFooty' style={{width:'65px', height:'65px'}}></Image>
            <Container className="navOptions" fluid >
                {
                    navOptions.map( (navOpt, idx) => (
                        <Link
                            key={idx}
                            to={`/${navOpt.link}`}
                            className={`navOption ${activeNavOption === navOpt.link ? 'active' : ''}`}
                            onClick={() => handleSelect(navOpt.link)}
                        >
                            {navOpt.icon}
                            {navOpt.title}
                        </Link>
                    ))
                }
            </Container>
            <Image src={Club} alt='club' style={{width:'75px', height:'75px'}}></Image>
        </Nav>
    );
};

export default VerticalNavBar;