import React, { useState } from "react";
import styled from "styled-components";
import { theme } from "../styles/theme";
import { Link } from "react-router-dom";

const Container = styled.div`
  max-width: 420px;
  margin: 60px auto;
  padding: 40px;
  background-color: white;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
  }
`;

const Title = styled.h1`
  font-size: 32px;
  font-weight: 800;
  color: ${theme.colors.text};
  margin-bottom: 16px;
  text-align: center;
  background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const Subtitle = styled.p`
  font-size: 16px;
  color: ${theme.colors.textSecondary};
  text-align: center;
  margin-bottom: 40px;
  line-height: 1.6;
`;

const SocialLoginContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
`;

const SocialButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  border: 1px solid ${theme.colors.border};
  border-radius: 16px;
  background-color: white;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      90deg,
      rgba(255, 107, 107, 0.1),
      rgba(78, 205, 196, 0.1)
    );
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-color: transparent;

    &::before {
      opacity: 1;
    }
  }

  &:active {
    transform: translateY(0);
  }
`;

const Divider = styled.div`
  display: flex;
  align-items: center;
  text-align: center;
  margin: 24px 0;
  color: ${theme.colors.textSecondary};
  font-size: 14px;
  font-weight: 500;

  &::before,
  &::after {
    content: "";
    flex: 1;
    border-bottom: 1px solid ${theme.colors.border};
  }

  &::before {
    margin-right: 16px;
  }

  &::after {
    margin-left: 16px;
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Input = styled.input`
  padding: 16px;
  border: 2px solid ${theme.colors.border};
  border-radius: 16px;
  font-size: 16px;
  transition: all 0.2s ease;
  background-color: ${theme.colors.lightGray};

  &:focus {
    outline: none;
    border-color: ${theme.colors.primary};
    background-color: white;
    box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.1);
  }

  &::placeholder {
    color: ${theme.colors.textSecondary};
  }
`;

const Label = styled.label`
  font-size: 14px;
  font-weight: 600;
  color: ${theme.colors.text};
  margin-left: 4px;
`;

const Button = styled.button`
  background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
  color: white;
  padding: 16px;
  border-radius: 16px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  margin-top: 8px;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, #4ecdc4, #ff6b6b);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

    &::before {
      opacity: 1;
    }
  }

  &:active {
    transform: translateY(0);
  }

  span {
    position: relative;
    z-index: 1;
  }
`;

const SignupContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid ${theme.colors.border};
`;

const SignupButton = styled(Link)`
  color: ${theme.colors.primary};
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 12px;
  transition: all 0.2s ease;
  background-color: rgba(255, 107, 107, 0.1);

  &:hover {
    background-color: rgba(255, 107, 107, 0.2);
    transform: translateY(-2px);
  }
`;

const HelperLinks = styled.div`
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 24px;
`;

const HelperLink = styled(Link)`
  color: ${theme.colors.textSecondary};
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  position: relative;

  &::after {
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
    transition: width 0.3s ease;
  }

  &:hover {
    color: ${theme.colors.primary};

    &::after {
      width: 100%;
    }
  }
`;

const LoginPage = () => {
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: 로그인 로직 구현
    console.log(formData);
  };

  return (
    <Container>
      <Title>라이언 커넥트</Title>
      <Subtitle>당신의 커리어를 연결하는 새로운 시작</Subtitle>

      {!showEmailForm ? (
        <>
          <SocialLoginContainer>
            <SocialButton>
              {/* <img
                src="/kakao-login_mediun_wide.png"
                alt="카카오"
                width="24"
                height="24"
              /> */}
              카카오로 계속하기
            </SocialButton>
            <SocialButton>
              {/* <img src="/google-icon.png" alt="구글" width="24" height="24" /> */}
              구글로 계속하기
            </SocialButton>
            <Divider>또는</Divider>
            <SocialButton onClick={() => setShowEmailForm(true)}>
              이메일로 계속하기
            </SocialButton>
          </SocialLoginContainer>

          <SignupContainer>
            <span
              style={{ color: theme.colors.textSecondary, fontSize: "14px" }}
            >
              계정이 없으신가요?
            </span>
            <div style={{ display: "flex", gap: "12px" }}>
              <SignupButton to="/signup/student">수료생 회원가입</SignupButton>
              <SignupButton to="/signup/company">기업 회원가입</SignupButton>
            </div>
          </SignupContainer>
        </>
      ) : (
        <>
          <Form onSubmit={handleSubmit}>
            <InputGroup>
              <Label>이메일</Label>
              <Input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="이메일을 입력하세요"
                required
              />
            </InputGroup>

            <InputGroup>
              <Label>비밀번호</Label>
              <Input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="비밀번호를 입력하세요"
                required
              />
            </InputGroup>

            <Button type="submit">
              <span>로그인</span>
            </Button>
          </Form>

          <HelperLinks>
            <HelperLink to="/find-id">아이디 찾기</HelperLink>
            <HelperLink to="/find-password">비밀번호 찾기</HelperLink>
          </HelperLinks>
        </>
      )}
    </Container>
  );
};

export default LoginPage;
