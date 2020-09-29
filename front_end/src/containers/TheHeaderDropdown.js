import React, {Component} from 'react'
import store from "../_helpers/store";
import { Link } from 'react-router-dom'

import {
    CBadge, CButton,
    CDropdown,
    CDropdownItem,
    CDropdownMenu,
    CDropdownToggle,
    CImg
} from '@coreui/react'
import CIcon from '@coreui/icons-react'

class TheHeaderDropdown extends Component {
    render () {
        const user = store.getState().authentication.user;
        return (
            <div>{user
                ?<CDropdown
                        inNav
                        className="c-header-nav-items mx-2"
                        direction="down"
                    >
                        <CDropdownToggle className="c-header-nav-link" caret={false}>
                            <CButton block color="dark">{user}</CButton>
                        </CDropdownToggle>
                        <CDropdownMenu className="pt-0" placement="bottom-end">
                            <CDropdownItem
                                header
                                tag="div"
                                color="light"
                                className="text-center"
                            >
                                <strong>Account</strong>
                            </CDropdownItem>
                            <CDropdownItem>
                                <CIcon name="cil-bell" className="mfe-2"/>
                                Updates
                                <CBadge color="info" className="mfs-auto">42</CBadge>
                            </CDropdownItem>
                            <CDropdownItem>
                                <CIcon name="cil-envelope-open" className="mfe-2"/>
                                Messages
                                <CBadge color="success" className="mfs-auto">42</CBadge>
                            </CDropdownItem>
                            <CDropdownItem>
                                <CIcon name="cil-task" className="mfe-2"/>
                                Tasks
                                <CBadge color="danger" className="mfs-auto">42</CBadge>
                            </CDropdownItem>
                            <CDropdownItem>
                                <CIcon name="cil-comment-square" className="mfe-2"/>
                                Comments
                                <CBadge color="warning" className="mfs-auto">42</CBadge>
                            </CDropdownItem>
                            <CDropdownItem
                                header
                                tag="div"
                                color="light"
                                className="text-center"
                            >
                                <strong>Settings</strong>
                            </CDropdownItem>
                            <CDropdownItem>
                                <CIcon name="cil-user" className="mfe-2"/>Profile
                            </CDropdownItem>
                            <CDropdownItem>
                                <CIcon name="cil-settings" className="mfe-2"/>
                                Settings
                            </CDropdownItem>
                            <CDropdownItem>
                                <CIcon name="cil-credit-card" className="mfe-2"/>
                                Payments
                                <CBadge color="secondary" className="mfs-auto">42</CBadge>
                            </CDropdownItem>
                            <CDropdownItem>
                                <CIcon name="cil-file" className="mfe-2"/>
                                Projects
                                <CBadge color="primary" className="mfs-auto">42</CBadge>
                            </CDropdownItem>
                            <CDropdownItem divider/>
                            <CDropdownItem>
                                <CIcon name="cil-lock-locked" className="mfe-2"/>
                                Lock Account
                            </CDropdownItem>
                        </CDropdownMenu>
                    </CDropdown>
                : <Link to={'/login'}> <CButton block color="info">Login</CButton></Link>}
            </div>
        )
    }
}

export default TheHeaderDropdown