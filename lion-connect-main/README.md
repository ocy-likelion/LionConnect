# ConnectLion Frontend

ConnectLion의 프론트엔드 레포지토리입니다.

## 🚀 기술 스택

- **React**: 18.2.0
- **React Router**: 6.22.0
- **Styled Components**: 6.1.8
- **React Icons**: 5.0.1
- **Axios**: 1.6.7

## 📁 프로젝트 구조

```
src/
├── components/     # 재사용 가능한 컴포넌트
├── pages/          # 페이지 컴포넌트
├── styles/         # 스타일 관련 파일
│   ├── theme.js    # 테마 설정
│   └── GlobalStyle.js  # 전역 스타일
├── utils/          # 유틸리티 함수
└── App.jsx         # 메인 앱 컴포넌트
```

## 🛠️ 개발 환경 설정

1. **의존성 설치**

```bash
npm install
```

2. **개발 서버 실행**

```bash
npm start
```

3. **빌드**

```bash
npm run build
```

## 🔧 주요 기능

### 1. 회원가입/로그인

- 이메일/비밀번호 기반 회원가입
- 소셜 로그인 (구글, 깃허브)
- JWT 기반 인증

### 2. 프로필 관리

- 개인 정보 수정
- 포트폴리오 관리
- 기술 스택 설정

### 3. 커뮤니티

- 게시글 CRUD
- 댓글 기능
- 좋아요/북마크

### 4. 매칭 시스템

- 프로필 기반 매칭
- 실시간 채팅
- 알림 시스템

## 📝 API 통신

### API 기본 설정

```javascript
// utils/api.js
import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// 요청 인터셉터
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 주요 API 엔드포인트

- 회원가입: `POST /api/auth/signup`
- 로그인: `POST /api/auth/login`
- 프로필 조회: `GET /api/users/profile`
- 게시글 목록: `GET /api/posts`
- 매칭 요청: `POST /api/matches`

## 🎨 스타일 가이드

### 테마 설정

```javascript
// styles/theme.js
export const theme = {
  colors: {
    primary: "#ff7710",
    secondary: "#ff8c00",
    white: "#ffffff",
    gray: "#666666",
    lightGray: "#f5f5f5",
    border: "#e0e0e0",
  },
  spacing: {
    xs: "0.25rem",
    sm: "0.5rem",
    md: "1rem",
    lg: "1.5rem",
    xl: "2rem",
    xxl: "3rem",
  },
  // ... 기타 테마 설정
};
```

### 컴포넌트 스타일링

- Styled Components 사용
- 테마 변수 활용
- 반응형 디자인 적용

## 🔄 상태 관리

### 주요 상태

- 사용자 인증 상태
- 프로필 정보
- 게시글 목록
- 매칭 상태

## 🧪 테스트

### 테스트 실행

```bash
npm test
```

### 테스트 커버리지 확인

```bash
npm run test:coverage
```

## 📦 배포

### 빌드 및 배포 과정

1. `npm run build`로 프로덕션 빌드
2. 빌드된 파일을 서버에 업로드
3. Nginx/Apache 설정

## 🤝 기여 가이드

1. 이슈 생성
2. 브랜치 생성 (`feature/기능명`)
3. 코드 작성 및 테스트
4. PR 생성
5. 코드 리뷰
6. 머지

## 📄 라이센스

MIT License

## 마이페이지 개발 가이드

### 1. 이력서 데이터 구조

```typescript
interface Resume {
  // 기본 정보
  name: string;
  introduction: string;
  email: string;
  phone: string;

  // 자기 소개
  selfIntroduction: string;

  // 업무 경험
  workExperience: Array<{
    company: string;
    department: string;
    position: string;
    isCurrent: boolean;
    description: string;
  }>;

  // 프로젝트
  projects: Array<{
    name: string;
    organization: string;
    period: string;
    description: string;
    image: File | null;
    isRepresentative: boolean;
  }>;

  // 포트폴리오
  portfolio: string;

  // 기술 스택
  skills: string[];

  // 학력
  education: Array<{
    university: string;
    major: string;
    period: string;
    description: string;
  }>;

  // 수상 및 활동
  awards: Array<{
    name: string;
    period: string;
    description: string;
  }>;

  // 자격증
  certificates: Array<{
    name: string;
    organization: string;
    date: string;
    number: string;
  }>;

  // 블로그 및 깃허브
  blog: string;
  github: string;
}
```

### 2. API 엔드포인트

```typescript
// 이력서 관련
GET /api/resumes/:userId          // 이력서 조회
POST /api/resumes                 // 이력서 생성
PUT /api/resumes/:resumeId        // 이력서 수정
DELETE /api/resumes/:resumeId     // 이력서 삭제

// 프로젝트 이미지 업로드
POST /api/resumes/projects/image  // 프로젝트 이미지 업로드
```

### 3. 데이터 검증 규칙

```typescript
// 기본 정보
name: {
  required: true,
  minLength: 2,
  maxLength: 50
},
email: {
  required: true,
  pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
},
phone: {
  required: true,
  pattern: /^[0-9-]+$/
},

// 업무 경험
workExperience: {
  company: {
    required: true,
    maxLength: 100
  },
  period: {
    required: true,
    pattern: /^\d{4}\.\d{2}\s*-\s*\d{4}\.\d{2}$/
  }
},

// 프로젝트
projects: {
  name: {
    required: true,
    maxLength: 100
  },
  image: {
    maxSize: 5 * 1024 * 1024, // 5MB
    allowedTypes: ['image/jpeg', 'image/png']
  }
}
```

### 4. 에러 처리

```typescript
// 에러 응답 형식
interface ErrorResponse {
  status: number;
  message: string;
  errors?: {
    [key: string]: string[];
  };
}

// 주요 에러 코드
400: '잘못된 요청',
401: '인증 실패',
403: '권한 없음',
404: '리소스 없음',
413: '파일 크기 초과',
415: '지원하지 않는 파일 형식',
500: '서버 오류'
```

### 5. 보안 고려사항

1. 모든 API 요청에 JWT 토큰 인증 필요
2. 파일 업로드 시 파일 크기와 형식 검증
3. 사용자별 데이터 접근 권한 검증
4. XSS 방지를 위한 입력값 검증
5. CSRF 토큰 사용

### 6. 성능 최적화

1. 이력서 데이터 캐싱
2. 이미지 리사이징 및 최적화
3. 페이지네이션 적용
4. 필요한 데이터만 조회하는 API 설계

### 7. 테스트 케이스

```typescript
// 단위 테스트 예시
describe("Resume API", () => {
  it("should create a new resume", async () => {
    // 테스트 코드
  });

  it("should validate resume data", async () => {
    // 테스트 코드
  });

  it("should handle file upload", async () => {
    // 테스트 코드
  });
});
```
