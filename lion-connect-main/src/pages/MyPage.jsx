import React, { useState } from "react";
import styled from "styled-components";
import { theme } from "../styles/theme";
import ResumeForm from "../components/ResumeForm";

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: ${theme.spacing.xl};
  display: flex;
  gap: ${theme.spacing.xl};
`;

const Sidebar = styled.div`
  width: 250px;
  background-color: ${theme.colors.white};
  border-radius: ${theme.borderRadius.lg};
  padding: ${theme.spacing.lg};
  box-shadow: ${theme.shadows.sm};
`;

const MenuItem = styled.div`
  padding: ${theme.spacing.md};
  margin-bottom: ${theme.spacing.sm};
  cursor: pointer;
  border-radius: ${theme.borderRadius.md};
  background-color: ${(props) =>
    props.active ? theme.colors.primary : "transparent"};
  color: ${(props) => (props.active ? theme.colors.white : theme.colors.text)};
  transition: ${theme.transitions.default};

  &:hover {
    background-color: ${(props) =>
      props.active ? theme.colors.primary : theme.colors.lightGray};
  }
`;

const Content = styled.div`
  flex: 1;
  background-color: ${theme.colors.white};
  border-radius: ${theme.borderRadius.lg};
  padding: ${theme.spacing.xl};
  box-shadow: ${theme.shadows.sm};
`;

const MyPage = () => {
  const [activeMenu, setActiveMenu] = useState("resume");

  return (
    <Container>
      <Sidebar>
        <MenuItem
          active={activeMenu === "resume"}
          onClick={() => setActiveMenu("resume")}
        >
          이력서 작성
        </MenuItem>
        <MenuItem
          active={activeMenu === "profile"}
          onClick={() => setActiveMenu("profile")}
          style={{ opacity: 0.5 }}
        >
          프로필 관리 (준비중)
        </MenuItem>
        <MenuItem
          active={activeMenu === "settings"}
          onClick={() => setActiveMenu("settings")}
          style={{ opacity: 0.5 }}
        >
          설정 (준비중)
        </MenuItem>
      </Sidebar>
      <Content>
        {activeMenu === "resume" && <ResumeForm />}
        {activeMenu === "profile" && (
          <div style={{ textAlign: "center", padding: "2rem" }}>
            준비중인 기능입니다.
          </div>
        )}
        {activeMenu === "settings" && (
          <div style={{ textAlign: "center", padding: "2rem" }}>
            준비중인 기능입니다.
          </div>
        )}
      </Content>
    </Container>
  );
};

export default MyPage;
