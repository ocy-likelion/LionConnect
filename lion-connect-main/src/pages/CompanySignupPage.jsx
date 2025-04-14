import React, { useState } from "react";
import styled from "styled-components";
import { theme } from "../styles/theme";
import { Link } from "react-router-dom";

const Container = styled.div`
  max-width: 500px;
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

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 24px;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Label = styled.label`
  font-size: 14px;
  font-weight: 600;
  color: ${theme.colors.text};
  margin-left: 4px;
`;

const Input = styled.input`
  padding: 16px;
  border: 2px solid ${theme.colors.border};
  border-radius: 16px;
  font-size: 16px;
  transition: all 0.2s ease;
  background-color: white;

  &:focus {
    outline: none;
    border-color: ${theme.colors.primary};
    box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.1);
  }

  &::placeholder {
    color: ${theme.colors.textSecondary};
  }
`;

const Select = styled.select`
  padding: 16px;
  border: 2px solid ${theme.colors.border};
  border-radius: 16px;
  font-size: 16px;
  transition: all 0.2s ease;
  background-color: white;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 16px center;
  background-size: 16px;

  &:focus {
    outline: none;
    border-color: ${theme.colors.primary};
    box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.1);
  }
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

const HelperText = styled.p`
  font-size: 12px;
  color: ${theme.colors.textSecondary};
  margin-top: 4px;
  margin-left: 4px;
`;

const BackLink = styled(Link)`
  display: flex;
  align-items: center;
  gap: 8px;
  color: ${theme.colors.text};
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 24px;
  transition: all 0.2s ease;

  &:hover {
    color: ${theme.colors.primary};
  }
`;

const CompanySignupPage = () => {
  const [formData, setFormData] = useState({
    companyName: "",
    email: "",
    password: "",
    confirmPassword: "",
    industry: "",
    companySize: "",
    website: "",
    description: "",
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
    // TODO: 회원가입 로직 구현
    console.log(formData);
  };

  return (
    <Container>
      <BackLink to="/login">
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
        로그인으로 돌아가기
      </BackLink>

      <Title>기업 회원가입</Title>
      <Subtitle>우수한 인재를 만나기 위한 첫 걸음</Subtitle>

      <Form onSubmit={handleSubmit}>
        <InputGroup>
          <Label>기업명</Label>
          <Input
            type="text"
            name="companyName"
            value={formData.companyName}
            onChange={handleChange}
            placeholder="기업명을 입력하세요"
            required
          />
        </InputGroup>

        <InputGroup>
          <Label>이메일</Label>
          <Input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="기업 이메일을 입력하세요"
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
          <HelperText>
            8자 이상, 영문, 숫자, 특수문자를 포함해야 합니다.
          </HelperText>
        </InputGroup>

        <InputGroup>
          <Label>비밀번호 확인</Label>
          <Input
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            placeholder="비밀번호를 다시 입력하세요"
            required
          />
        </InputGroup>

        <InputGroup>
          <Label>산업군</Label>
          <Select
            name="industry"
            value={formData.industry}
            onChange={handleChange}
            required
          >
            <option value="">산업군을 선택하세요</option>
            <option value="IT">IT/소프트웨어</option>
            <option value="finance">금융/보험</option>
            <option value="manufacturing">제조/생산</option>
            <option value="service">서비스</option>
            <option value="retail">유통/판매</option>
            <option value="education">교육</option>
            <option value="healthcare">의료/바이오</option>
            <option value="other">기타</option>
          </Select>
        </InputGroup>

        <InputGroup>
          <Label>기업 규모</Label>
          <Select
            name="companySize"
            value={formData.companySize}
            onChange={handleChange}
            required
          >
            <option value="">기업 규모를 선택하세요</option>
            <option value="1-10">1-10명</option>
            <option value="11-50">11-50명</option>
            <option value="51-200">51-200명</option>
            <option value="201-500">201-500명</option>
            <option value="501-1000">501-1000명</option>
            <option value="1000+">1000명 이상</option>
          </Select>
        </InputGroup>

        <InputGroup>
          <Label>기업 웹사이트</Label>
          <Input
            type="url"
            name="website"
            value={formData.website}
            onChange={handleChange}
            placeholder="https://"
          />
        </InputGroup>

        <InputGroup>
          <Label>기업 소개</Label>
          <Input
            type="text"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="기업을 간단히 소개해주세요"
            required
          />
        </InputGroup>

        <Button type="submit">
          <span>회원가입 완료</span>
        </Button>
      </Form>
    </Container>
  );
};

export default CompanySignupPage;
